from budger.libs.dynamic_fields import DynamicFieldsModelSerializer
from .models import Annual, Event
from rest_framework import serializers
from budger.directory.serializers import EntityListShortSerializer, KsoDepartment1Serializer


class AnnualSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Annual
        fields = '__all__'


class EventSerializer(DynamicFieldsModelSerializer):
    responsible_department_obj = serializers.SerializerMethodField()
    controlled_entities_obj = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = '__all__'

    def get_responsible_department_obj(self, obj):
        return KsoDepartment1Serializer(obj.responsible_department).data

    def get_controlled_entities_obj(self, obj):
        return EntityListShortSerializer(obj.controlled_entities, many=True).data

    def validate(self, attrs):
        if attrs['reason'] == 2:
            if 'appeal_author' in attrs:
                attrs['appeal_author'] = None
            if 'appeal_number' in attrs:
                attrs['appeal_number'] = None
            if 'appeal_date' in attrs:
                attrs['appeal_date'] = None
            if 'initiator' in attrs:
                attrs['initiator'] = None

        if len(attrs['attendant_departments']) > 0 and attrs['mode'] == 2:
            raise serializers.ValidationError({'mode': 'Event have attendant departments. Event mode can not be 2'})

        if attrs['period_to'] < attrs['period_from']:
            raise serializers.ValidationError({'period_to': 'period_to must occur after period_from'})

        return attrs
