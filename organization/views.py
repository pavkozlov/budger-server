from rest_framework import generics
from .models import OrganizationCommon
from .serializers import OrganizationCommonListSerializer, OrganizationCommonRetrieveSerializer
from rest_framework import filters


class OrganizationCommonListView(generics.ListAPIView):
    """
    GET Список организаций из ЕГРЮЛ
    """
    serializer_class = OrganizationCommonListSerializer
    queryset = OrganizationCommon.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']


class OrganizationCommonRetrieveView(generics.RetrieveAPIView):
    """
    GET Сведения об организации из ЕГРЮЛ
    """
    serializer_class = OrganizationCommonRetrieveSerializer

    def get_queryset(self):
        queryset = OrganizationCommon.objects.all()
        return queryset

