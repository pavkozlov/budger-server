from rest_framework import serializers
from organization.models.organization_common import OrganizationCommon
from organization.models.organization_kso import OrganizationKso
from organization.models.employee import Employee
from budger.dyna_fields import DynamicFieldsModelSerializer


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class OrganizationKsoSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = OrganizationKso
        fields = '__all__'

    employees = EmployeeSerializer(
        many=True
    )


class OrganizationCommonSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = OrganizationCommon
        fields = '__all__'

    organization_kso = OrganizationKsoSerializer(
        read_only=True
    )
