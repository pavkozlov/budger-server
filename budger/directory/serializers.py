from rest_framework import serializers
from budger.libs.dynamic_fields import DynamicFieldsModelSerializer
from .models.entity import Entity
from .models.kso import Kso, KsoDepartment1, KsoEmployee


class EntitySerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Entity
        fields = '__all__'


class KsoDepartment1Serializer(serializers.ModelSerializer):
    class Meta:
        model = KsoDepartment1
        fields = ('id', 'title', 'sub_departments')

    class _KsoDepartment2Serializer(serializers.ModelSerializer):
        class Meta:
            model = KsoDepartment1
            fields = ('id', 'title')

    sub_departments = _KsoDepartment2Serializer(many=True)


class KsoOgrnField(serializers.RelatedField):
    def to_representation(self, value):
        try:
            obj = Entity.objects.get(ogrn=value)
            entity = EntitySerializer(obj).data
        except Entity.DoesNotExist:
            entity = None
        return {'ogrn_number': value, 'entity': entity}


class KsoSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Kso
        fields = '__all__'

    ogrn = KsoOgrnField(read_only=True)
    departments = KsoDepartment1Serializer(many=True)


class KsoEmployeeListSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = KsoEmployee
        fields = '__all__'

    class _KsoSerializer(serializers.ModelSerializer):
        class Meta:
            model = Kso
            fields = ['id', 'title_short', 'title_full']

    kso = _KsoSerializer()


class KsoEmployeeRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = KsoEmployee
        exclude = ('department2',)

    class _KsoSerializer(serializers.ModelSerializer):
        class Meta:
            model = Kso
            fields = ('id', 'title_full', 'title_short')

    kso = _KsoSerializer()
    department1 = KsoDepartment1Serializer()
