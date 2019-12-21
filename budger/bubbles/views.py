from rest_framework import views, generics
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.response import Response
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
        inspection = self.request.query_params.get('_filter__inspection')

        qs = Aggregation.objects.all()

        if inspection == '1':
            qs = Aggregation.objects.get_entities_by_inspection(AggregationManager.INSPECTION_1)
        if inspection == '2':
            qs = Aggregation.objects.get_entities_by_inspection(AggregationManager.INSPECTION_2)
        if inspection == '3':
            qs = Aggregation.objects.get_entities_by_inspection(AggregationManager.INSPECTION_3)
        if inspection == '4':
            qs = Aggregation.objects.get_entities_by_inspection(AggregationManager.INSPECTION_4)
        if inspection == '5':
            qs = Aggregation.objects.get_entities_by_inspection(AggregationManager.INSPECTION_5)
        if inspection == '6':
            qs = Aggregation.objects.get_entities_by_inspection(AggregationManager.INSPECTION_6)

        return qs

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
                    'amount_plan': m.regproj_amount_plan,
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

        for obj in queryset:
            key = f'{obj.entity.id}-{obj.year}'
            if key in buff:
                buff[key] = self._merge_models(
                    buff[key],
                    self._transform_model(obj)
                )
            else:
                buff[key] = self._transform_model(obj)

        serializer = self.get_serializer(
            [buff[k] for k in buff],
            many=True
        )

        return Response(serializer.data)
