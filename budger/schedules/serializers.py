from budger.libs.dynamic_fields import DynamicFieldsModelSerializer
from .models import Annual, Event


class AnnualSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Annual
        fields = '__all__'


class EventSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
