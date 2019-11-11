"""
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
"""
from rest_framework import generics, filters, response, views
from budger.directory.models.entity import Entity, FoundersTree
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
    GET Список организаций из ЕГРЮЛ/ЕГРИП
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
    GET Сведения об организации из ЕГРЮЛ/ЕГРИП.
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
    GET Список всех сотрудников КСО и подразделений, имеющих право являться отвестсвенными за мероприятия
    """
    def get(self, request):
        result = {}
        kso = request.user.ksoemployee.kso

        employees = KsoEmployee.objects.filter(kso=kso, can_be_responsible=True)
        departments = KsoDepartment1.objects.filter(kso=kso, can_participate_in_events=True)

        result['departments'] = KsoResponsiblesDepartment1Serializer(departments, many=True).data
        result['employees'] = KsoResponsiblesEmployeeSerializer(employees, many=True).data

        return response.Response(result)


class EntityFoundersTreeRetrieveView(generics.RetrieveAPIView):
    """
    GET Граф дочерних ЮЛ, учрежденных выбранным ЮЛ и его потомками.
    """
    def retrieve(self, request, *args, **kwargs):
        entity_id = kwargs['pk']
        founders_tree = FoundersTree.objects.get(entity_id=entity_id)
        return response.Response(founders_tree.data)
