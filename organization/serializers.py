from rest_framework import serializers
from .models import OrganizationKso, OrganizationCommon, Employee
from budger.dyna_fields import DynamicFieldsModelSerializer


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class OrganizationKsoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationKso
        fields = ('id', 'title', 'employees')
        read_only_fields = ('id',)

    employees = EmployeeSerializer(
        many=True,
        read_only=True
    )


class OrganizationCommonListSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = OrganizationCommon
        fields = '__all__'


class OrganizationCommonRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationCommon
        fields = '__all__'

    organization_kso = OrganizationKsoSerializer(
        read_only=True
    )
