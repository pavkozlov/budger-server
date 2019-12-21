from rest_framework import serializers
from .models import Aggregation
from budger.directory.serializers import EntityShortSerializer


class AggregationSerializer(serializers.ModelSerializer):
    entity = EntityShortSerializer()
    projects = serializers.ListField()
    violations = serializers.ListField()

    class Meta:
        model = Aggregation
        fields = ('year', 'entity', 'projects', 'violations',
                  'budget_amount_plan', 'budget_amount_fact')
