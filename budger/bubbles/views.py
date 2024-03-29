from rest_framework import views, generics
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.response import Response
import budger.definitions as defs
from .data import NatProject, RegProject
from .models import Aggregation
from .managers import AggregationManager
from .serializers import AggregationSerializer
from .filters import AggregationFilter


class NatProjectsView(views.APIView):
    """
    GET Список национальных проектов.
    """
    def get(self, request):
        return Response(NatProject.list())


class RegProjectsView(views.APIView):
    """
    GET Список региональных проектов.
    @_filter__grbs - филтр проектов пр ГРБС
    """
    def get(self, request, *args, **kwargs):

        if kwargs.get('pk') is not None:
            # Вернуть данные о выбранном регпроекте
            p = RegProject.get_by_id(kwargs['pk'])
            if p:
                return Response(p)

        if request.query_params.get('_filter__grbs'):
            grbs_id = int(request.query_params.get('_filter__grbs'))
            p_list = RegProject.get_by_grbs(grbs_id)
            return Response([RegProject.transform(p) for p in p_list])

        return Response(status=HTTP_404_NOT_FOUND)


class AggregationView(generics.ListAPIView):
    """
    GET Поиск объектов контроля в рамках РОП.
        @_filter__inspection             - номер инспекции.
        @_filter__year                   - год, за который производится поиск (возможно несколько значений через зпт)

        @_filter__budget_amount_plan     - минимальный порог запланированного бюджета *.
        @_filter__budget_amount_fact     - минимальный порог исполненного бюджета *.

        @_filter__violations_count       - количество выявленных нарушений *.
        @_filter__violations_amount      - выявленные нарушения в денежном экв. *.

        @_filter__regproj_participant    - участие в рег. проектах

        * (выбираем ОК только со значениями, большими указанного)
    """
    serializer_class = AggregationSerializer
    filter_backends = [AggregationFilter]
    pagination_class = None

    def get_queryset(self):
        # TODO: эту хрень можно смело двигать в filters

        qs = None

        if self.request.query_params.get('_filter__inspection') is not None:
            inspection = self.request.query_params.get('_filter__inspection')
            inspections = inspection.split(',') if ',' in inspection else [inspection]

            for inspection in inspections:
                dep1 = None

                if inspection == '1':
                    dep1 = defs.INSPECTION_1_ID
                elif inspection == '2':
                    dep1 = defs.INSPECTION_2_ID
                elif inspection == '3':
                    dep1 = defs.INSPECTION_3_ID
                elif inspection == '4':
                    dep1 = defs.INSPECTION_4_ID
                elif inspection == '5':
                    dep1 = defs.INSPECTION_5_ID
                elif inspection == '6':
                    dep1 = defs.INSPECTION_6_ID

                if dep1 is not None:
                    qs1 = Aggregation.objects.get_entities_by_inspection(dep1)
                    qs = qs1 if qs is None else qs | qs1

        return qs if qs is not None else Aggregation.objects.all()

    @staticmethod
    def _transform_model(m):
        m.projects = []
        m.violations = []

        if m.regproj_participant is True:
            tokens = m.memo.split('/')
            m.projects.append({
                'title': tokens[0].strip(),
                'results': [{
                    'title': tokens[1].strip(),
                    'amount_plan_fed': m.regproj_amount_plan_fed,
                    'amount_plan_local': m.regproj_amount_plan_local,
                    'amount_plan_gos': m.regproj_amount_plan_gos,
                    'amount_plan_out': m.regproj_amount_plan_out,
                    'amount_fact': m.regproj_amount_fact,
                    'amount_recd': m.regproj_amount_recd
                }]
            })

        if m.violations_count is not None or m.violations_amount is not None:
            tokens = m.memo.split('/')
            m.violations.append({
                'count': m.violations_count,
                'amount': m.violations_amount,
                'event_title': tokens[0].strip(),
                'event_type': tokens[1].strip(),
            })

        return m

    @staticmethod
    def _merge_models(m1, m2):
        """
        Объединение двух моделей.
        """
        if m2.budget_amount_plan is not None:
            m1.budget_amount_plan = m2.budget_amount_plan

        if m2.budget_amount_fact is not None:
            m1.budget_amount_fact = m2.budget_amount_fact

        if m2.projects:
            p2 = m2.projects[0]
            f = False

            for p1 in m1.projects:
                if p1['title'] == p2['title']:
                    p1['results'] += p2['results']
                    f = True
                    break

            if f is False:
                m1.projects.append(m2.projects[0])

        if m2.violations:
            m1.violations += m2.violations
        return m1

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        buff = {}

        # Группировка записей по объекту/году

        for obj in queryset:
            key = '{}-{}'.format(obj.entity.id, obj.year)

            if key in buff:
                buff[key] = self._merge_models(
                    buff[key],
                    self._transform_model(obj)
                )
            else:
                buff[key] = self._transform_model(obj)

        result = [buff[k] for k in buff]

        # А тут блять надо фильтровать _filter__regproj_participant=(true|false)

        if request.query_params.get('_filter__regproj_participant') == 'true':
            result1 = []
            for obj in result:
                if len(obj.projects) > 0:
                    result1.append(obj)
            result = result1

        elif request.query_params.get('_filter__regproj_participant') == 'false':
            result1 = []
            for obj in result:
                if len(obj.projects) == 0:
                    result1.append(obj)
            result = result1

        # А тут блять надо фильтровать _filter__revision_participant=(true|false)

        if request.query_params.get('_filter__revision_participant') == 'true':
            result1 = []
            for obj in result:
                if len(obj.violations) > 0:
                    result1.append(obj)
            result = result1

        elif request.query_params.get('_filter__revision_participant') == 'false':
            result1 = []
            for obj in result:
                if len(obj.violations) == 0:
                    result1.append(obj)
            result = result1

        # А еще блять надо фильтрануть по сумме количеств нарушений
        if request.query_params.get('_filter__violations_count_min') is not None:
            result1 = []
            for obj in result:
                vs = 0
                if len(obj.violations) > 0:
                    for v in obj.violations:
                        vs += v.get('count', 0)
                if vs >= int(request.query_params.get('_filter__violations_count_min', 0)):
                    result1.append(obj)
            result = result1

        if request.query_params.get('_filter__violations_count_max') is not None:
            result1 = []
            for obj in result:
                vs = 0
                if len(obj.violations) > 0:
                    for v in obj.violations:
                        vs += v.get('count', 0)
                if vs <= int(request.query_params.get('_filter__violations_count_max', 0)):
                    result1.append(obj)
            result = result1

        serializer = self.get_serializer(result, many=True)

        return Response(serializer.data)
