from rest_framework import serializers
from budger.libs.dynamic_fields import DynamicFieldsModelSerializer
from .models import Annual, Event


class ScheduleSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Annual
        fields = '__all__'


class EventSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
