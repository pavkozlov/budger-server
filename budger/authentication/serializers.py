from rest_framework import serializers
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User, Permission
from budger.directory.models.kso import KsoEmployee

from budger.directory.serializers import KsoSerializer
from budger.directory.serializers import KsoDepartment1WithHeadSerializer


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('key',)


class UserSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()

    def get_permissions(self, obj):
        res = []
        for p in obj.user_permissions.all():
            res.append(p.codename)
        return res

    class Meta:
        model = User
        fields = ('id', 'email', 'groups', 'permissions', 'is_superuser')


class KsoEmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    kso = KsoSerializer()
    department1 = KsoDepartment1WithHeadSerializer()

    class Meta:
        model = KsoEmployee
        fields = '__all__'
