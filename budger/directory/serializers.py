from rest_framework import serializers
from budger.libs.dynamic_fields import DynamicFieldsModelSerializer
from django.contrib.auth.models import User
from .models.entity import Entity, MunicipalBudget
from .models.kso import Kso, KsoDepartment1, KsoDepartment2, KsoEmployee


def grbs_type(obj):
    t1 = obj.kbk_title.upper()
    t2 = t1 + ' МОСКОВСКОЙ ОБЛАСТИ'  # бгг
    if obj.title_full.upper() in [t1, t2]:
        if obj.budget_lvl_code == '31' or obj.budget_lvl_code == '32':
            return 'municipal'
        else:
            return 'regional'
    return None


class EntityListSerializer(DynamicFieldsModelSerializer):
    grbs_type = serializers.SerializerMethodField()

    class Meta:
        model = Entity
        fields = (
            'id', 'reg_date', 'title_full', 'title_short', 'inn', 'ogrn',
            'head_position', 'head_name', 'ofk_code', 'org_status_code', 'spec_event_code', 'grbs_type'
        )

    def get_grbs_type(self, obj):
        return grbs_type(obj)


class EntityShortSerializer(serializers.ModelSerializer):
    grbs_type = serializers.SerializerMethodField()

    class Meta:
        model = Entity
        fields = ('id', 'title_full', 'inn', 'ogrn', 'ofk_code', 'org_status_code', 'grbs_type')

    def get_grbs_type(self, obj):
        return grbs_type(obj)


class EntitySubordinatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = (
            'id',
            'title_full',
            'inn', 'ogrn', 'ofk_code', 'kbk_code',
            'head_name', 'head_position',
            'subordinates'
        )


class EntitySerializer(serializers.ModelSerializer):
    grbs_type = serializers.SerializerMethodField()

    def get_grbs_type(self, obj):
        return grbs_type(obj)

    class Meta:
        model = Entity
        fields = '__all__'


class KsoEmployeeShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = KsoEmployee
        fields = ('id', 'name', 'position', 'photo_slug',)


class KsoEmployeeSuperiorsSerializer(serializers.ModelSerializer):
    class _KsoDepartment1Serializer(serializers.ModelSerializer):
        class Meta:
            model = KsoDepartment1
            fields = ('id', 'title',)

    class _KsoDepartment2Serializer(serializers.ModelSerializer):
        class Meta:
            model = KsoDepartment2
            fields = ('id', 'title',)

    class Meta:
        model = KsoEmployee
        fields = ('id', 'name', 'position', 'photo_slug', 'department1', 'department2')

    department1 = _KsoDepartment1Serializer()
    department2 = _KsoDepartment2Serializer()


class KsoDepartment1ShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = KsoDepartment1
        fields = ('id', 'title',)


class KsoDepartment2ShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = KsoDepartment1
        fields = ('id', 'title',)


class KsoDepartment1Serializer(serializers.ModelSerializer):
    sub_departments = KsoDepartment2ShortSerializer(many=True)

    class Meta:
        model = KsoDepartment1
        fields = ('id', 'title', 'sub_departments')


class KsoDepartment1WithHeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = KsoDepartment1
        fields = ('id', 'title', 'head', 'curator')

    class _KsoEmployeeShortSerializer(serializers.ModelSerializer):
        class Meta:
            model = KsoEmployee
            fields = ('id', 'name', 'position', 'photo_slug')

    head = _KsoEmployeeShortSerializer()
    curator = _KsoEmployeeShortSerializer()


class KsoListSerializer(DynamicFieldsModelSerializer):
    head = KsoEmployeeShortSerializer()
    employees_count_fact = serializers.SerializerMethodField()

    class Meta:
        model = Kso
        fields = (
            'id', 'title_short', 'head', 'in_alliance',
            'employees_count_staff', 'employees_count_fact'
        )

    def get_employees_count_fact(self, obj):
        count = KsoEmployee.objects.filter(kso=obj, inactive_title=None).count()
        return count


class KsoShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kso
        fields = ('id', 'title_short')


class KsoMediumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kso
        fields = ('id', 'title_short', 'addr_fact')


class KsoSerializer(serializers.ModelSerializer):
    entity = EntitySerializer()
    departments = KsoDepartment1Serializer(many=True)
    head = KsoEmployeeShortSerializer()
    employees_count_fact = serializers.SerializerMethodField()

    class Meta:
        model = Kso
        exclude = ('title_search',)

    def get_employees_count_fact(self, obj):
        count = KsoEmployee.objects.filter(kso=obj, inactive_title=None).count()
        return count


class KsoEmployeeListSerializer(DynamicFieldsModelSerializer):
    kso = KsoShortSerializer()

    class Meta:
        model = KsoEmployee
        fields = '__all__'


class KsoEmployeeSerializer(serializers.ModelSerializer):
    kso = KsoMediumSerializer()
    department1 = KsoDepartment1ShortSerializer()
    department2 = KsoDepartment2ShortSerializer()

    class Meta:
        model = KsoEmployee
        fields = '__all__'

    def to_internal_value(self, employee):
        if type(employee.get('kso')) is int:
            obj = Kso.objects.get(pk=employee['kso'])
            employee['kso'] = obj

        if type(employee.get('department1')) is int:
            obj = KsoDepartment1.objects.get(pk=employee['department1'])
            employee['department1'] = obj

        if type(employee.get('department2')) is int:
            obj = KsoDepartment2.objects.get(pk=employee['department2'])
            employee['department2'] = obj

        if type(employee.get('user')) is int:
            obj = User.objects.get(pk=employee['user'])
            employee['user'] = obj

        return employee


class MunicipalBudgetSerializer(serializers.ModelSerializer):
    title_full = serializers.SerializerMethodField()
    administration = EntityListSerializer()

    def get_title_full(self, obj):
        return obj.title_display

    class Meta:
        model = MunicipalBudget
        fields = ('title_full', 'subordinates', 'code', 'administration')
