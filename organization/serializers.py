from rest_framework import serializers
from .models import OrganizationKso, OrganizationCommon, Employee


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('id', 'name',)


class OrganizationKsoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationKso
        fields = ('id', 'title', 'employees')
        read_only_fields = ('id',)

    employees = EmployeeSerializer(
        many=True,
        read_only=True
    )


class OrganizationCommonListSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationCommon
        fields = ('id', 'title',)
        read_only_fields = ('id',)


class OrganizationCommonRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationCommon
        fields = ('id', 'title', 'ogrn', 'inn', 'organization_kso')
        read_only_fields = ('id',)

    organization_kso = OrganizationKsoSerializer(read_only=True)
