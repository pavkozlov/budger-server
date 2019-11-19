from rest_framework import serializers
from budger.libs.dynamic_fields import DynamicFieldsModelSerializer
from .models.entity import Entity, MunicipalBudget
from .models.kso import Kso, KsoDepartment1, KsoEmployee


########################################################################################################################
# Entity serializers
########################################################################################################################


class EntityListSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Entity
        fields = (
            'id', 'reg_date', 'title_full', 'title_short', 'inn', 'ogrn',
            'head_position', 'head_name', 'ofk_code'
        )


class EntityShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = ('id', 'title_full', 'title_short', 'inn', 'ogrn', 'ofk_code')


class EntitySubordinatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = ('id', 'title_full', 'title_short', 'inn', 'ogrn', 'ofk_code', 'kbk_code', 'subordinates')


class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = '__all__'


########################################################################################################################
# Kso departments serializers
########################################################################################################################


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


########################################################################################################################
# Kso serializers
########################################################################################################################


class KsoListSerializer(DynamicFieldsModelSerializer):
    head = serializers.DictField()
    employees_count_fact = serializers.IntegerField()

    class Meta:
        model = Kso
        fields = (
            'id', 'title_short', 'head', 'in_alliance',
            'employees_count_staff', 'employees_count_fact'
        )


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


########################################################################################################################
# Kso employee serializers
########################################################################################################################


class KsoEmployeeListSerializer(DynamicFieldsModelSerializer):
    kso = KsoShortSerializer()

    class Meta:
        model = KsoEmployee
        fields = '__all__'


class KsoEmployeeMediumSerializer(serializers.ModelSerializer):
    kso = KsoMediumSerializer()
    department1 = KsoDepartment1Serializer()

    class Meta:
        model = KsoEmployee
        exclude = ('department2',)


class KsoEmployeeShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = KsoEmployee
        fields = ('id', 'name', 'position',)


#
# MunicipalBudgetTitle serializers
#


class MunicipalBudgetSerializer(serializers.ModelSerializer):
    title_full = serializers.SerializerMethodField()

    def get_title_full(self, obj):
        return obj.title_display

    class Meta:
        model = MunicipalBudget
        fields = ('title_full', 'subordinates', 'code',)
