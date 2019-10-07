from rest_framework import generics, filters
from organization.models.organization_common import OrganizationCommon
from organization.models.organization_kso import OrganizationKso
from .serializers import OrganizationCommonSerializer
from .serializers import OrganizationKsoSerializer
from budger.dyna_fields import DynaFieldsListAPIView


class OrganizationCommonListView(DynaFieldsListAPIView):
    """
    GET Список организаций из ЕГРЮЛ
    """
    serializer_class = OrganizationCommonSerializer
    queryset = OrganizationCommon.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['title_full', 'title_short', 'inn']


class OrganizationCommonRetrieveView(generics.RetrieveAPIView):
    """
    GET Сведения об организации из ЕГРЮЛ
    """
    serializer_class = OrganizationCommonSerializer
    queryset = OrganizationCommon.objects.all()


class OrganizationKsoView(DynaFieldsListAPIView):
    """
    GET Список организаций из ЕГРЮЛ
    """
    serializer_class = OrganizationKsoSerializer
    queryset = OrganizationKso.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['title_full', 'title_short', 'inn']
