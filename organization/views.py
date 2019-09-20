from rest_framework import generics
from .models import OrganizationCommon, OrganizationKso, Employee
from .serializers import OrganizationCommonSerializer, OrganizationKsoSerializer, EmployeeSerializer
from rest_framework.response import Response


class OrganizationCommonView(generics.ListAPIView):
    """
    GET Список организаций из ЕГРЮЛ
    """
    serializer_class = OrganizationCommonSerializer

    def get_queryset(self):
        queryset = OrganizationCommon.objects.all()
        return queryset

    def post(self, request):
        queryset = self.get_queryset()
        serializer = OrganizationCommonSerializer(queryset, many=True)
        return Response(serializer.data)
