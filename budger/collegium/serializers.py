from rest_framework import serializers
from .models import Meeting, Speaker


class SpeakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Speaker
        fields = '__all__'


class MeetingSerializer(serializers.ModelSerializer):
    speakers = SpeakerSerializer(many=True, read_only=True)

    class Meta:
        model = Meeting
        fields = ['id', 'exec_date', 'status', 'speakers']
