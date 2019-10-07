from rest_framework import generics, filters
from .models import OrganizationCommon
from .serializers import OrganizationCommonListSerializer, OrganizationCommonRetrieveSerializer
from budger.dyna_fields import DynaFieldsListView


class OrganizationCommonListView(DynaFieldsListView):
    """
    GET Список организаций из ЕГРЮЛ
    """
    serializer_class = OrganizationCommonListSerializer
    queryset = OrganizationCommon.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['title_full', 'title_short', 'inn']


class OrganizationCommonRetrieveView(generics.RetrieveAPIView):
    """
    GET Сведения об организации из ЕГРЮЛ
    """
    serializer_class = OrganizationCommonRetrieveSerializer
    queryset = OrganizationCommon.objects.all()
