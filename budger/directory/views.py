from rest_framework import generics, filters
from budger.directory.models.entity import Entity
from budger.directory.models.kso import Kso, KsoEmployee
from budger.libs.dynamic_fields import DynaFieldsListAPIView
from budger.libs.pagination import UnlimitedResultsSetPagination
from .serializers import EntitySerializer, KsoSerializer, KsoEmployeeListSerializer, KsoEmployeeRetrieveSerializer


class EntityListView(DynaFieldsListAPIView):
    """
    GET Список организаций из ЕГРЮЛ
    """
    serializer_class = EntitySerializer
    queryset = Entity.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['title_full', 'title_short', 'inn']


class EntityRetrieveView(generics.RetrieveAPIView):
    """
    GET Сведения об организации из ЕГРЮЛ
    """
    serializer_class = EntitySerializer
    queryset = Entity.objects.all()


class KsoListView(DynaFieldsListAPIView):
    """
    GET Список КСО
    """
    serializer_class = KsoSerializer
    queryset = Kso.objects.all()
    pagination_class = UnlimitedResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['title_full', 'title_short']


class KsoRetrieveView(generics.RetrieveAPIView):
    """
    GET Сведения о выбранном КСО
    """
    serializer_class = KsoSerializer
    queryset = Kso.objects.all()
    filter_backends = [filters.SearchFilter]


class KsoEmployeeListView(DynaFieldsListAPIView):
    """
    GET Список сотрудников КСО
    """
    serializer_class = KsoEmployeeListSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        queryset = KsoEmployee.objects.all()

        kso_id = self.request.query_params.get('kso_id', None)
        if kso_id is not None:
            queryset = queryset.filter(kso__id=kso_id)

        return queryset

class KsoEmployeeRetrieveView(generics.RetrieveAPIView):
    """
    GET Сведения о выбранном сотруднике КСО
    """
    serializer_class = KsoEmployeeRetrieveSerializer
    queryset = KsoEmployee.objects.all()
    filter_backends = [filters.SearchFilter]
