from rest_framework import serializers
from budger.libs.dynamic_fields import DynamicFieldsModelSerializer
from .models.entity import Entity, MunicipalBudget
from .models.kso import Kso, KsoDepartment1, KsoDepartment2, KsoEmployee


class EntityListSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Entity
        fields = (
            'id', 'reg_date', 'title_full', 'title_short', 'inn', 'ogrn',
            'head_position', 'head_name', 'ofk_code', 'org_status_code', 'spec_event_code',
        )


class EntityShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = ('id', 'title_full', 'title_short', 'inn', 'ogrn', 'ofk_code', 'org_status_code')


class EntitySubordinatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = ('id', 'title_full', 'title_short', 'inn', 'ogrn', 'ofk_code', 'kbk_code', 'subordinates')


class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = '__all__'


class KsoEmployeeShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = KsoEmployee
        fields = ('id', 'name', 'position', 'photo_slug',)


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
        count = KsoEmployee.objects.filter(kso=obj).count()
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
        count = KsoEmployee.objects.filter(kso=obj).count()
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

        return employee


class MunicipalBudgetSerializer(serializers.ModelSerializer):
    title_full = serializers.SerializerMethodField()

    def get_title_full(self, obj):
        return obj.title_display

    class Meta:
        model = MunicipalBudget
        fields = ('title_full', 'subordinates', 'code',)
