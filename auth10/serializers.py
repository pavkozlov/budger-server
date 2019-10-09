from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User as AuthUser
from organization.serializers import EmployeeSerializer
from .models import User


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('key',)


class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = ('id', 'email', 'groups', 'user_permissions',)


class UserSerializer(serializers.ModelSerializer):
    auth_user = AuthUserSerializer()
    employee = EmployeeSerializer()

    class Meta:
        model = User
        fields = '__all__'
