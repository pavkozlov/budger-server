from rest_framework import generics, filters
from budger.directory.models.entity import Entity
from budger.directory.models.kso import Kso
from budger.libs.dynamic_fields import DynaFieldsListAPIView
from .serializers import EntitySerializer
from .serializers import KsoSerializer


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
    filter_backends = [filters.SearchFilter]
    search_fields = ['title_full', 'title_short']


class KsoRetrieveView(generics.RetrieveAPIView):
    """
    GET Сведения о выбранном КСО
    """
    serializer_class = KsoSerializer
    queryset = Kso.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['title_full', 'title_short']
