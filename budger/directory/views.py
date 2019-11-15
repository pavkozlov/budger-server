"""
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
"""

from django.shortcuts import get_object_or_404
from rest_framework import generics, filters, response, status, views
from budger.directory.models.entity import Entity, EntitySubordinates
from budger.directory.models.kso import Kso, KsoEmployee, KsoDepartment1
from budger.libs.dynamic_fields import DynaFieldsListAPIView
from budger.libs.pagination import UnlimitedResultsSetPagination
from .serializers import (
    EntityListSerializer,
    EntityRetrieveSerializer,
    KsoListSerializer,
    KsoRetrieveSerializer,
    KsoEmployeeListSerializer,
    KsoEmployeeRetrieveSerializer,
    KsoResponsiblesEmployeeSerializer,
    KsoResponsiblesDepartment1Serializer,
)
from .filters import EntityFilter


class EntityListView(DynaFieldsListAPIView):
    """
    GET Список объектов контроля
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
    serializer_class = EntityRetrieveSerializer
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
    serializer_class = KsoRetrieveSerializer
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
    serializer_class = KsoEmployeeRetrieveSerializer
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
            'departments': KsoResponsiblesDepartment1Serializer(departments, many=True).data,
            'employees': KsoResponsiblesEmployeeSerializer(employees, many=True).data
        })


class EntitySubordinatesView2Delete(views.APIView):
    """
    GET Граф подчиненных объектов котроля.
    @inn -- ИНН объекта, для которого требуется вывести граф.
    """
    def get(self, request):
        if 'inn' not in request.query_params:
            return response.Response(
                {"detail": "@inn не определен."},
                status=status.HTTP_400_BAD_REQUEST
            )

        inn = request.query_params['inn']
        entity = get_object_or_404(Entity, inn=inn)
        subordinates = EntitySubordinates.objects.get(entity_id=entity.id)
        return response.Response(subordinates.tree)


class EntitySubordinatesView(views.APIView):
    lookup_field = 'ofk_code'

    """
    GET Граф подчиненных объектов контроля.
    @ofk_code — ОФК-код объекта, для которого требуется вывести граф.
    """
    def get(self, request, ofk_code):
        entity = get_object_or_404(Entity, ofk_code=ofk_code)
        subordinates = get_object_or_404(EntitySubordinates, entity_id=entity.id)
        return response.Response(subordinates.tree)


class EntityMunicipalsView(DynaFieldsListAPIView):
    """
    GET Список муниципальных объектов контроля.
    """
    serializer_class = EntityListSerializer
    filter_backends = [EntityFilter]
    queryset = Entity.objects.filter(opf_code__startswith=754, org_status_code__in=[1, 4])
    """
    queryset = Entity.objects.filter(
        title_full__istartswith='АДМИНИСТРАЦИЯ ГОРОДСКОГО ОКРУГА ',
        org_status_code__in=[1, 4]
    )
    """
