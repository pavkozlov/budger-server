from rest_framework import serializers
from .models import Event, Department


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    responsible_department_obj = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = (
            'title',
            'responsible_department',
            'attendant_departments',
            'responsible_department_obj',
        )

    def get_responsible_department_obj(self, obj):
        return DepartmentSerializer(obj.responsible_department).data
