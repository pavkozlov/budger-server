from rest_framework import serializers
from records.models import Record, Tag
from budger.serializers import UserSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'title')


class RecordSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    user = UserSerializer()

    class Meta:
        model = Record
        fields = ('id', 'title', 'description', 'amount', 'created', 'updated', 'user', 'tags')


class TokenSerializer(serializers.Serializer):
    """
    Serializes the token data
    """
    token = serializers.CharField(max_length=255)
