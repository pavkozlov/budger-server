from rest_framework import serializers
from .models import Meeting, Speaker
from budger.directory.serializers import KsoEmployeeShortSerializer


class SpeakerSerializer(serializers.ModelSerializer):
    employee = KsoEmployeeShortSerializer()

    class Meta:
        model = Speaker
        fields = ['id', 'subjects', 'employee']


class MeetingSerializer(serializers.ModelSerializer):
    speakers = SpeakerSerializer(many=True, read_only=True)

    class Meta:
        model = Meeting
        fields = ['id', 'exec_date', 'status', 'speakers']
