from rest_framework import serializers
from .models import OrganizationKso, OrganizationCommon, Employee


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('id', 'name',)


class OrganizationKsoSerializer(serializers.ModelSerializer):

    class EmployeesRelatedField(serializers.RelatedField):
        def to_representation(self, obj):
            return {
                'id': obj.pk,
                'name': obj.name,
            }

    employees = EmployeesRelatedField(
        many=True,
        read_only=True
    )

    class Meta:
        model = OrganizationKso
        fields = ('id', 'title', 'employees')
        read_only_fields = ('id',)


class OrganizationCommonSerializer(serializers.ModelSerializer):
    organization_kso = OrganizationKsoSerializer()

    class Meta:
        model = OrganizationCommon
        fields = ('id', 'title', 'ogrn', 'inn', 'organization_kso')
        read_only_fields = ('id',)
