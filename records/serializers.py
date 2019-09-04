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
        fields = ('id', 'title', 'description', 'created', 'updated', 'user', 'tags')


class RecordSerializerListItem(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Record
        fields = ('id', 'title', 'created', 'tags')
