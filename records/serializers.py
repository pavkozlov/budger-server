from rest_framework import serializers

from django.contrib.auth.models import User
from records.models import Record, Tag


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


# Serializers define the API representation.
class RecordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Record
        fields = ('id', 'title', 'description', 'created', 'updated', 'user', 'tags')


# Serializers define the API representation.
class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'title')
