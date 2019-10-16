from rest_framework import serializers
from budger.libs.dynamic_fields import DynamicFieldsModelSerializer
from .models.entity import Entity
from .models.kso import Kso, KsoDepartment, KsoEmployee


class EntitySerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Entity
        fields = '__all__'


class KsoDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = KsoDepartment
        fields = ('id', 'title')


class KsoSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Kso
        fields = '__all__'

    departments = KsoDepartmentSerializer(many=True)


class KsoEmployeeListSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = KsoEmployee
        fields = '__all__'

    class _KsoSerializer(serializers.ModelSerializer):
        class Meta:
            model = Kso
            fields = ['id', 'title_full']

    kso = _KsoSerializer()


class KsoEmployeeRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = KsoEmployee
        fields = '__all__'

    kso = KsoSerializer()
