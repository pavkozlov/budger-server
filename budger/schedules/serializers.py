from budger.libs.dynamic_fields import DynamicFieldsModelSerializer
from .models import Annual, Event, Workflow
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


class EventSerializer(serializers.ModelSerializer):
    # controlled_entities = EntityListShortSerializer(many=True)

    class Meta:
        model = Event
        fields = '__all__'

    def to_representation(self, instance):
        repr = super(EventSerializer, self).to_representation(instance)

        repr['responsible_employee'] = KsoEmployeeShortSerializer(
            instance.responsible_employee
        ).data

        repr['responsible_department'] = KsoDepartment1ShortSerializer(
            instance.responsible_department
        ).data

        repr['attendant_departments'] = KsoDepartment1ShortSerializer(
            instance.attendant_departments.all(),
            many=True
        ).data

        repr['controlled_entities'] = EntityShortSerializer(
            instance.controlled_entities.all(),
            many=True
        ).data

        repr['attendant_ksos_parallel'] = KsoShortSerializer(
            instance.attendant_ksos_parallel.all(),
            many=True
        ).data

        repr['attendant_ksos_together'] = KsoShortSerializer(
            instance.attendant_ksos_together.all(),
            many=True
        ).data

        return repr

    def validate(self, attrs):
        if attrs.get('period_to', None) is not None and attrs.get('period_from', None) is not None:
            if attrs['period_to'] <= attrs['period_from']:
                raise serializers.ValidationError({'message': 'Period range setup error.'})

        if attrs.get('type') == 1 and attrs.get('group') not in [1, 2, 3, 4]:
            raise serializers.ValidationError({'group': 'Invalid group for this event type'})
        elif attrs.get('type') == 2 and attrs.get('group') not in [5, 6, 7, 8]:
            raise serializers.ValidationError({'group': 'Invalid group for this event type'})

        return attrs


class EventShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'title')


class WorkflowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workflow
        fields = '__all__'


class WorkflowQuerySerializer(serializers.ModelSerializer):
    sender = KsoEmployeeShortSerializer()
    recipient = KsoEmployeeShortSerializer()
    event = EventShortSerializer()

    class Meta:
        model = Workflow
        fields = '__all__'
