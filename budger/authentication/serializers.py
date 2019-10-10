from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
# from budger.directory.serializers import KsoEmployeeSerializer
from .models import Profile


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('key',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'groups', 'user_permissions',)


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    # employee = KsoEmployeeSerializer()()

    class Meta:
        model = Profile
        fields = '__all__'
