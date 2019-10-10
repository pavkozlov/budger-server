from rest_framework import serializers
from budger.libs.dynamic_fields import DynamicFieldsModelSerializer
from .models.entity import Entity
from .models.kso import Kso, KsoEmployee


class KsoEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = KsoEmployee
        fields = '__all__'


class KsoSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Kso
        fields = '__all__'

    employees = KsoEmployeeSerializer(
        many=True
    )


class EntitySerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Entity
        fields = '__all__'
