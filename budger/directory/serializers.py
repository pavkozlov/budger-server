from rest_framework import serializers
from budger.libs.dynamic_fields import DynamicFieldsModelSerializer
from .models.entity import Entity
from .models.kso import Kso, KsoDepartment1, KsoEmployee


class EntitySerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Entity
        fields = '__all__'

    class _EntitySerializer(serializers.ModelSerializer):
        class Meta:
            model = Entity
            fields = ('id', 'inn', 'title_full', 'title_short')

    founders = _EntitySerializer(many=True)


class KsoDepartment1Serializer(serializers.ModelSerializer):
    class Meta:
        model = KsoDepartment1
        fields = ('id', 'title', 'sub_departments')

    class _KsoDepartment2Serializer(serializers.ModelSerializer):
        class Meta:
            model = KsoDepartment1
            fields = ('id', 'title')

    sub_departments = _KsoDepartment2Serializer(many=True)


class KsoListSerializer(serializers.ModelSerializer):
    head = serializers.DictField()

    class Meta:
        model = Kso
        fields = (
            'id', 'title_full', 'worker_count_fact',
            'worker_count_staff', 'in_alliance', 'head'
        )


class KsoRetrieveSerializer(DynamicFieldsModelSerializer):
    entity = EntitySerializer()
    departments = KsoDepartment1Serializer(many=True)
    head = serializers.SerializerMethodField()
    worker_count_fact = serializers.SerializerMethodField()

    class Meta:
        model = Kso
        exclude = ('title_search',)

    def get_head(self, obj):
        try:
            employee = KsoEmployee.objects.get(kso=obj, is_head=True)
            return {
                'name': employee.name,
                'position': employee.position,
                'photo_slug': employee.photo_slug
            }
        except KsoEmployee.DoesNotExist:
            return None
        except KsoEmployee.MultipleObjectsReturned:
            return None

    def get_worker_count_fact(self, obj):
        employees = KsoEmployee.objects.filter(kso=obj).count()
        return employees


class KsoEmployeeListSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = KsoEmployee
        fields = '__all__'

    class _KsoSerializer(serializers.ModelSerializer):
        class Meta:
            model = Kso
            fields = ('id', 'title_full')

    kso = _KsoSerializer()


class KsoEmployeeRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = KsoEmployee
        exclude = ('department2',)

    class _KsoSerializer(serializers.ModelSerializer):
        class Meta:
            model = Kso
            fields = ('id', 'title_full')

    kso = _KsoSerializer()
    department1 = KsoDepartment1Serializer()
