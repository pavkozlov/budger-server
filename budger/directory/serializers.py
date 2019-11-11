from rest_framework import serializers
from budger.libs.dynamic_fields import DynamicFieldsModelSerializer
from .models.entity import Entity, FoundersTree
from .models.kso import Kso, KsoDepartment1, KsoEmployee


class EntityListSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Entity
        fields = (
            'id', 'reg_date', 'title_full', 'title_short', 'inn', 'ogrn',
            'head_position', 'head_name_last', 'head_name_first', 'head_name_second'
        )


class EntityRetrieveSerializer(DynamicFieldsModelSerializer):
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


class KsoListSerializer(serializers.ModelSerializer):
    head = serializers.DictField()
    employees_count_fact = serializers.IntegerField()

    class Meta:
        model = Kso
        fields = (
            'id', 'title_short', 'head', 'in_alliance',
            'employees_count_staff', 'employees_count_fact'
        )


class KsoRetrieveSerializer(DynamicFieldsModelSerializer):
    entity = EntityRetrieveSerializer()
    departments = KsoDepartment1Serializer(many=True)
    head = serializers.SerializerMethodField()
    employees_count_fact = serializers.SerializerMethodField()

    class Meta:
        model = Kso
        exclude = ('title_search',)

    def get_head(self, obj):
        try:
            employee = KsoEmployee.objects.get(kso=obj, is_head=True)
            return {
                'id': employee.id,
                'name': employee.name,
                'position': employee.position,
                'photo_slug': employee.photo_slug
            }
        except KsoEmployee.DoesNotExist:
            return None
        except KsoEmployee.MultipleObjectsReturned:
            return None

    def get_employees_count_fact(self, obj):
        count = KsoEmployee.objects.filter(kso=obj).count()
        return count


class KsoEmployeeListSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = KsoEmployee
        fields = '__all__'

    class _KsoSerializer(serializers.ModelSerializer):
        class Meta:
            model = Kso
            fields = ('id', 'title_short')

    kso = _KsoSerializer()


class KsoResponsiblesEmployeeSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = KsoEmployee
        fields = ('id', 'name')


class KsoResponsiblesDepartment1Serializer(serializers.ModelSerializer):
    class Meta:
        model = KsoDepartment1
        fields = ('id', 'title')


class KsoEmployeeRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = KsoEmployee
        exclude = ('department2',)

    class _KsoSerializer(serializers.ModelSerializer):
        class Meta:
            model = Kso
            fields = ('id', 'title_full', 'addr_fact')

    kso = _KsoSerializer()
    department1 = KsoDepartment1Serializer()
