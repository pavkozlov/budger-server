from rest_framework import generics, filters, response
from budger.directory.models.entity import Entity, FoundersTree
from budger.directory.models.kso import Kso, KsoEmployee
from budger.libs.dynamic_fields import DynaFieldsListAPIView
from budger.libs.pagination import UnlimitedResultsSetPagination
from .serializers import (
    EntityListSerializer,
    EntityRetrieveSerializer,
    KsoListSerializer,
    KsoRetrieveSerializer,
    KsoEmployeeListSerializer,
    KsoEmployeeRetrieveSerializer,
    FoundersTreeSerialiser,
)
from .filters import EntityFilter


class EntityListView(DynaFieldsListAPIView):
    """
    GET Список организаций из ЕГРЮЛ/ЕГРИП
    """
    serializer_class = EntityListSerializer
    filter_backends = [EntityFilter]
    queryset = Entity.objects.all()


class EntityRetrieveView(generics.RetrieveAPIView):
    """
    GET Сведения об организации из ЕГРЮЛ/ЕГРИП
    """
    serializer_class = EntityRetrieveSerializer
    queryset = Entity.objects.all()


class KsoListView(DynaFieldsListAPIView):
    """
    GET Список КСО
    """
    serializer_class = KsoListSerializer
    queryset = Kso.objects.list()
    pagination_class = UnlimitedResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['title_search']


class KsoRetrieveView(generics.RetrieveAPIView):
    """
    GET Сведения о выбранном КСО
    """
    serializer_class = KsoRetrieveSerializer
    queryset = Kso.objects.all()


class KsoEmployeeListView(DynaFieldsListAPIView):
    """
    GET Список сотрудников КСО.
    @_filter__title - поиск по полям 'title_full', 'title_short'
    @_filter__inn - фильтр по полю inn
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

    def options(self, request, *args, **kwargs):
        """
        Don't include the view description in OPTIONS responses.
        """
        meta = self.metadata_class()
        data = meta.determine_metadata(request, self)
        data.pop('description')
        return data


class KsoEmployeeRetrieveView(generics.RetrieveAPIView):
    """
    GET Сведения о выбранном сотруднике КСО
    """
    serializer_class = KsoEmployeeRetrieveSerializer
    queryset = KsoEmployee.objects.all()


class EntityFoundersTreeRetrieveView(generics.RetrieveAPIView):
    def retrieve(self, request, *args, **kwargs):
        entity_id = kwargs['pk']
        founders_tree = FoundersTree.objects.get(entity_id=entity_id)
        return response.Response(founders_tree.data)
