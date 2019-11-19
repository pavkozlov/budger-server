"""
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
"""

from django.shortcuts import get_object_or_404
from rest_framework import generics, filters, response, status, views
from budger.directory.models.entity import Entity
from budger.directory.models.kso import Kso, KsoEmployee, KsoDepartment1
from budger.libs.dynamic_fields import DynaFieldsListAPIView
from budger.libs.pagination import UnlimitedResultsSetPagination
from .serializers import (
    EntityShortSerializerWithSubordinates, EntityListSerializer, EntitySerializer,
    KsoListSerializer,
    KsoSerializer,
    KsoEmployeeListSerializer,
    KsoEmployeeMediumSerializer,
    KsoEmployeeShortSerializer,
    KsoDepartment1ShortSerializer,
)
from .filters import EntityFilter


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
    """
    serializer_class = KsoListSerializer
    queryset = Kso.objects.list()
    pagination_class = UnlimitedResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['title_search']


class KsoRetrieveView(generics.RetrieveAPIView):
    """
    GET Сведения о выбранном КСО.
    """
    serializer_class = KsoSerializer
    queryset = Kso.objects.all()


class KsoEmployeeListView(DynaFieldsListAPIView):
    """
    GET Список сотрудников КСО.
    @_filter__kso_id - фильтр по полю kso.id
    """
    serializer_class = KsoEmployeeListSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        queryset = KsoEmployee.objects.order_by('name')

        kso_id = self.request.query_params.get('kso_id', None)
        if kso_id is not None:
            queryset = queryset.filter(kso__id=kso_id).order_by('name')

        return queryset


class KsoEmployeeRetrieveView(generics.RetrieveAPIView):
    """
    GET Сведения о выбранном сотруднике КСО
    """
    serializer_class = KsoEmployeeMediumSerializer
    queryset = KsoEmployee.objects.all()


class KsoResponsiblesView(views.APIView):
    """
    GET Список сотрудников и подразделений КСО, могущих являться отвестсвенными за мероприятия
    """
    def get(self, request):
        kso = request.user.ksoemployee.kso

        employees = KsoEmployee.objects.filter(kso=kso, can_be_responsible=True)
        departments = KsoDepartment1.objects.filter(kso=kso, can_participate_in_events=True)

        return response.Response({
            'departments': KsoDepartment1ShortSerializer(departments, many=True).data,
            'employees': KsoEmployeeShortSerializer(employees, many=True).data
        })


class EntityRegionalsView(views.APIView):
    """
    GET Список муниципальных объектов контроля - ГРБС.
    """
    def get(self, request):
        queryset = Entity.objects.filter(
            opf_code__in=['75201', '75203', '75204'],
            org_status_code__in=['1', '4'],
            parent_id__isnull=True,
            org_type_code__in=['01', '02'],
            budget_lvl_code__in=['20', '50'],
        )
        serializer = EntityShortSerializerWithSubordinates(queryset, many=True)
        return response.Response(serializer.data)


class EntityMunicipalsView(views.APIView):
    """
    GET Список муниципальных объектов контроля.
    """

    def get(self, request):
        queryset = Entity.objects.filter(
            budget_lvl_code__in=['31', '32'],
            okogu_code__in=['3300100', '3300200'],
            org_status_code__in=['1', '4']
        ).distinct()


class EntitySubordinatesView(views.APIView):
    """
    GET Список подчиненных объектов контроля.
    """
    def get(self, request, pk):
        entity = get_object_or_404(Entity, pk=pk)
        subordinates = Entity.objects.filter(pk__in=entity.subordinates)
        serializer = EntityShortSerializerWithSubordinates(subordinates, many=True)
        return response.Response(serializer.data)
