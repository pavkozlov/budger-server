from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
# from budger.directory.serializers import KsoEmployeeSerializer
from budger.directory.models.kso import KsoEmployee
from budger.directory.serializers import KsoSerializer, KsoDepartment1Serializer


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('key',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'groups', 'user_permissions',)


class KsoEmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    kso = KsoSerializer()
    department1 = KsoDepartment1Serializer()

    class Meta:
        model = KsoEmployee
        fields = '__all__'
