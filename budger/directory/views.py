"""
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
"""

import os
from django.db import connection
from django.shortcuts import get_object_or_404
from rest_framework import generics, filters, views, parsers, status
from rest_framework.response import Response
from budger.libs.dynamic_fields import DynaFieldsListAPIView
from budger.libs.shortcuts import normalize_search_str
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

        return Response(status=response_status)


class KsoResponsiblesView(views.APIView):
    """
    GET Список подразделений КСО, могущих являться отвестсвенными за мероприятия
    """

    def get(self, request):
        kso = request.user.ksoemployee.kso
        departments = KsoDepartment1.objects.filter(kso=kso, can_participate_in_events=True)
        serializer = KsoDepartment1WithHeadSerializer(departments, many=True)

        return Response({'departments': serializer.data})


class EntityRegionalsView(views.APIView):
    """
    GET Список муниципальных объектов контроля - ГРБС.
    """
    def get(self, request):
        qs = Entity.objects.filter(
            parent_id__isnull=True,
            opf_code__in=['75201', '75203', '75204'],
            org_type_code__in=['01', '02'],
            budget_lvl_code__in=['20', '50'],
            org_status_code__in=['1', '4'],
        )

        serializer = EntitySubordinatesSerializer(qs, many=True)
        return Response(serializer.data)


class EntityMunicipalsView(views.APIView):
    """
    GET Список групп верхнего уровня муниципальных объектов контроля.
    @_filter__budget_code Список муниципальных объектов контроля с заданным budget_code.
    """
    def get(self, request):
        # TODO: move to filters.py?
        fi_budget = request.query_params.get('_filter__budget_code')

        if fi_budget is not None:
            parent = get_object_or_404(MunicipalBudget, code=fi_budget)
            qs = Entity.objects.filter(pk__in=parent.subordinates)
            serializer = EntitySubordinatesSerializer(qs, many=True)
        else:
            qs = MunicipalBudget.objects.all()
            serializer = MunicipalBudgetSerializer(qs, many=True)

        return Response(serializer.data)


class EntitySubordinatesView(views.APIView):
    """
    GET Список муниципальных объектов контроля - ГРБС.
    """
    def get(self, request, pk):
        parent = get_object_or_404(Entity, pk=pk)
        queryset = Entity.objects.filter(pk__in=parent.subordinates)
        serializer = EntitySubordinatesSerializer(queryset, many=True)
        return Response(serializer.data)


class EmployeeSuperiorsView(views.APIView):
    """
    GET Список руководителей работника.
    """
    def get(self, request, pk):
        employee = get_object_or_404(KsoEmployee, id=pk)
        superiors = employee.get_superiors()
        serializer = KsoEmployeeSuperiorsSerializer(superiors, many=True)
        return Response(serializer.data)


class EntityAggregationsView(views.APIView):
    """
    GET агрегатор единого реестра объектов контроля.
        @_filter__1 - фильтр по названию / ИНН / ОГРН / имя руководителя
        @_filter__municipals - рабатать только с подмножеством "муниципальные ОК"
        @_filter__regionals - рабатать только с подмножеством "региональные ОК"
    """
    def get(self, request):
        cursor = connection.cursor()

        sql = 'SELECT opf_code, COUNT(id) AS cnt FROM directory_entity {} GROUP BY opf_code ORDER BY cnt DESC'
        where_sql_stat = ''
        params = []

        if request.query_params.get('_filter__1') is not None:
            fi = normalize_search_str(request.query_params['_filter__1'])

            where_sql_stat = '''
                WHERE (
                    UPPER(title_search) LIKE UPPER(%s) OR
                    inn LIKE %s OR
                    ogrn LIKE %s OR
                    UPPER(head_name) LIKE UPPER(%s)
                )
            '''

            params += ['%{}%'.format(fi), '%{}%'.format(fi), '%{}%'.format(fi), '%{}%'.format(fi)]

        if request.query_params.get('_filter__group') == 'municipals':
            where_sql_stat += ' WHERE ' if where_sql_stat == '' else ' AND '
            where_sql_stat += 'id=ANY(ARRAY(SELECT data FROM directory_entitygroup WHERE code = \'municipals\'))'

        if request.query_params.get('_filter__group') == 'regionals':
            where_sql_stat += ' WHERE ' if where_sql_stat == '' else ' AND '
            where_sql_stat += 'id=ANY(ARRAY(SELECT data FROM directory_entitygroup WHERE code = \'regionals\'))'

        cursor.execute(sql.format(where_sql_stat), params)

        return Response({
            opf_code: count for opf_code, count in cursor.fetchall()
        })


class EnumsView(views.APIView):
    """
    GET Список констант
    """

    def get(self, request):
        return Response({
            'SPEC_EVENT_CODE_ENUM': SPEC_EVENT_CODE_ENUM
        })
