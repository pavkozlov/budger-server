"""
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
"""

from django.db import connection
import os
from django.shortcuts import get_object_or_404
from rest_framework import generics, filters, response, views, parsers, status
from django.db.models import Q
from budger.libs.dynamic_fields import DynaFieldsListAPIView
import budger.app_settings as app_settings
from .models.entity import Entity, MunicipalBudget, SPEC_EVENT_CODE_ENUM
from .models.kso import Kso, KsoEmployee, KsoDepartment1
from .permissions import CanUpdateEmployee

from .serializers import (
    EntitySubordinatesSerializer, EntityListSerializer, EntitySerializer,
    KsoListSerializer, KsoSerializer,
    KsoEmployeeListSerializer,
    KsoEmployeeSerializer,
    KsoEmployeeSuperiorsSerializer,
    MunicipalBudgetSerializer,
    KsoDepartment1WithHeadSerializer
)

from .filters import EntityFilter, KsoEmployeeFilter
from .renderers import KsoEmployeeCsvRenderer


class EntityListView(DynaFieldsListAPIView):
    """
    GET Список объектов контроля.
    @_filter__title
    @_filter__inn
    """
    serializer_class = EntityListSerializer
    filter_backends = [EntityFilter]
    queryset = Entity.objects.all()

    """
    @method_decorator(cache_page(60 * 60 * 2))
    def list(self, request):
        return super().list(request)
    """


class EntityRetrieveView(generics.RetrieveAPIView):
    """
    GET Сведения об объекте контроля.
    """
    serializer_class = EntitySerializer
    queryset = Entity.objects.all()


class KsoListView(DynaFieldsListAPIView):
    """
    GET Список КСО.
    @search
    """
    serializer_class = KsoListSerializer
    queryset = Kso.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['title_search']
    paginator = None


class KsoRetrieveView(generics.RetrieveAPIView):
    """
    GET Сведения о выбранном КСО.
    """
    serializer_class = KsoSerializer
    queryset = Kso.objects.all()


class KsoEmployeeListView(DynaFieldsListAPIView):
    """
    GET         Список сотрудников КСО.
    @search - поиск по имени
    @_filter__kso_id - фильтр по полю kso.id
    @_filter__name - фильтр по имени
    """
    serializer_class = KsoEmployeeListSerializer
    filter_backends = [filters.SearchFilter, KsoEmployeeFilter]
    search_fields = ['name']
    queryset = KsoEmployee.objects.filter(is_developer=False)


class KsoEmployeeListCsv(DynaFieldsListAPIView):
    """
    GET Список всех сотрудников КСО, отрендеренные в csv
    """
    serializer_class = KsoEmployeeListSerializer
    renderer_classes = [KsoEmployeeCsvRenderer, ]
    queryset = KsoEmployee.objects.filter(is_developer=False)


class KsoEmployeeRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    """
    GET Сведения о выбранном сотруднике КСО
    PUT Обновление данных выбранного сотрудника КСО
    """
    serializer_class = KsoEmployeeSerializer
    queryset = KsoEmployee.objects.all()
    permission_classes = [CanUpdateEmployee]


class KsoEmployeeUploadPhotoView(views.APIView):
    """
    PUT Загрузить файл с фото работника. Обязателен заголовок Content-Disposition:inline;filename={photo.jpg}
    """
    parser_classes = (parsers.FileUploadParser,)
    permission_classes = [CanUpdateEmployee]

    def put(self, request, *args, **kwargs):
        response_status = status.HTTP_400_BAD_REQUEST
        employee_id = kwargs.get('pk')

        if employee_id is not None:
            employee = get_object_or_404(KsoEmployee, pk=employee_id)
            photo_file = request.FILES['file']

            if photo_file.content_type.lower() in ('image/jpeg', 'image/png'):
                # Prepare to save image
                path = app_settings.EMPLOYEE_PHOTO_DIR

                name = 'employee_{}'.format(employee_id)
                if photo_file.content_type.lower() == 'image/jpeg':
                    name += '.jpg'
                if photo_file.content_type.lower() == 'image/png':
                    name += '.png'

                # Save image
                with open(os.path.join(path, name), 'wb') as file:
                    file.write(photo_file.read())

                # Update Employee model
                employee.photo_slug = name
                employee.save()

                response_status = status.HTTP_204_NO_CONTENT

        return response.Response(status=response_status)


class KsoResponsiblesView(views.APIView):
    """
    GET Список подразделений КСО, могущих являться отвестсвенными за мероприятия
    """

    def get(self, request):
        kso = request.user.ksoemployee.kso
        departments = KsoDepartment1.objects.filter(kso=kso, can_participate_in_events=True)
        data = KsoDepartment1WithHeadSerializer(departments, many=True).data

        return response.Response({'departments': data})


class EntityRegionalsView(views.APIView):
    """
    GET Список муниципальных объектов контроля - ГРБС.
    @_filter__title__inn Фильтр по названию и ИНН.
    """

    def get(self, request):
        terms = request.query_params.get('_filter__title__inn', None)

        if terms is not None:
            queryset = Entity.objects.filter(
                (Q(title_search__icontains=terms) | Q(inn=terms)) &
                Q(budget_lvl_code__in=['20', '50'])
            )
        else:
            queryset = Entity.objects.filter(
                parent_id__isnull=True,
                opf_code__in=['75201', '75203', '75204'],
                org_type_code__in=['01', '02'],
                budget_lvl_code__in=['20', '50'],
                org_status_code__in=['1', '4'],
            )

        data = EntitySubordinatesSerializer(queryset, many=True).data
        return response.Response(data)


class EntityMunicipalsView(views.APIView):
    """
    GET Список групп верхнего уровня муниципальных объектов контроля.
    @_filter__budget_code Список муниципальных объектов контроля с заданным budget_code.
    @_filter__title__inn Фильтр по названию и ИНН.
    """

    def get(self, request):
        terms_budget = request.query_params.get('_filter__budget_code', None)
        terms_title = request.query_params.get('_filter__title__inn', None)

        if terms_budget is not None:
            parent = get_object_or_404(MunicipalBudget, code=terms_budget)
            queryset = Entity.objects.filter(pk__in=parent.subordinates)
            data = EntitySubordinatesSerializer(queryset, many=True).data

        elif terms_title is not None:
            queryset = Entity.objects.filter(
                (Q(title_search__icontains=terms_title) | Q(inn=terms_title)) &
                Q(budget_lvl_code__in=['31', '32'])
            )
            data = EntitySubordinatesSerializer(queryset, many=True).data

        else:
            queryset = MunicipalBudget.objects.all()
            data = MunicipalBudgetSerializer(queryset, many=True).data

        return response.Response(data)


class EntitySubordinatesView(views.APIView):
    """
    GET Список муниципальных объектов контроля - ГРБС.
    """
    def get(self, request, pk):
        parent = get_object_or_404(Entity, pk=pk)
        queryset = Entity.objects.filter(pk__in=parent.subordinates)
        data = EntitySubordinatesSerializer(queryset, many=True).data
        return response.Response(data)


class EmployeeSuperiorsView(views.APIView):
    def get(self, request, pk):
        employee = get_object_or_404(KsoEmployee, id=pk)
        superiors = employee.get_superiors()
        serializer = KsoEmployeeSuperiorsSerializer(superiors, many=True)
        return response.Response(serializer.data)


class EntityAggregationsView(views.APIView):
    """
    GET агрегатор единого реестра объектов контроля.
    """
    def get(self, request):
        cursor = connection.cursor()

        sql = 'SELECT opf_code, COUNT(id) AS cnt FROM directory_entity {} GROUP BY opf_code ORDER BY cnt DESC'
        where_sql_stat = ''
        params = None

        if request.query_params.get('_filter__title') is not None:
            title = request.query_params['_filter__title']
            params = ('%{}%'.format(title),)
            where_sql_stat = 'WHERE UPPER(title_search) LIKE UPPER(%s)'

        cursor.execute(sql.format(where_sql_stat), params)

        return response.Response({
            opf_code: count for opf_code, count in cursor.fetchall()
        })


class EnumsView(views.APIView):
    """
    GET Список констант
    """

    def get(self, request):
        return response.Response({
            'SPEC_EVENT_CODE_ENUM': SPEC_EVENT_CODE_ENUM
        })
