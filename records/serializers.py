from rest_framework import serializers

from django.contrib.auth.models import User
from records.models import Record, Tag


# Serializers define the API representation.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


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
