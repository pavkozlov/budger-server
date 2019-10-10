from rest_framework import generics, filters
from organization.models.organization import Organization
from organization.models.organization_kso import OrganizationKso
from budger.libs.dynamic_fields import DynaFieldsListAPIView
from .serializers import OrganizationSerializer
from .serializers import OrganizationKsoSerializer


class OrganizationListView(DynaFieldsListAPIView):
    """
    GET Список организаций из ЕГРЮЛ
    """
    serializer_class = OrganizationSerializer
    queryset = Organization.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['title_full', 'title_short', 'inn']


class OrganizationRetrieveView(generics.RetrieveAPIView):
    """
    GET Сведения об организации из ЕГРЮЛ
    """
    serializer_class = OrganizationSerializer
    queryset = Organization.objects.all()


class OrganizationKsoListView(DynaFieldsListAPIView):
    """
    GET Список КСО
    """
    serializer_class = OrganizationKsoSerializer
    queryset = OrganizationKso.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['title_full', 'title_short']


class OrganizationKsoRetrieveView(generics.RetrieveAPIView):
    """
    GET Сведения о выбранном КСО
    """
    serializer_class = OrganizationKsoSerializer
    queryset = OrganizationKso.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['title_full', 'title_short']
