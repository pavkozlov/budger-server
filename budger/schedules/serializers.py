from budger.libs.dynamic_fields import DynamicFieldsModelSerializer
from .models import Annual, Event
from rest_framework import serializers
from budger.directory.serializers import (
    KsoShortSerializer,
    EntityShortSerializer,
    KsoDepartment1ShortSerializer,
    KsoEmployeeShortSerializer
)


########################################################################################################################
# Annual serializers
########################################################################################################################


class AnnualListSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Annual
        fields = '__all__'


########################################################################################################################
# Event serializers
########################################################################################################################


class EventListSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class EventFullSerializer(serializers.ModelSerializer):
    # controlled_entities = EntityListShortSerializer(many=True)

    class Meta:
        model = Event
        fields = '__all__'

    def to_representation(self, instance):
        repr = super(EventFullSerializer, self).to_representation(instance)

        repr['responsible_employee'] = KsoEmployeeShortSerializer(
            instance.responsible_employee,
        ).data

        repr['responsible_department'] = KsoDepartment1ShortSerializer(
            instance.responsible_department,
        ).data

        repr['attendant_departments'] = KsoDepartment1ShortSerializer(
            instance.attendant_departments.all(),
            many=True
        ).data

        repr['controlled_entities'] = EntityShortSerializer(
            instance.controlled_entities.all(),
            many=True
        ).data

        repr['attendant_ksos'] = KsoShortSerializer(
            instance.attendant_ksos.all(),
            many=True
        ).data

        return repr

    def validate(self, attrs):
        if attrs['period_to'] <= attrs['period_from']:
            raise serializers.ValidationError({'message': 'Period range setup error.'})

        return attrs
