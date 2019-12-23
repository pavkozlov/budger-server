from rest_framework import serializers
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User

from budger.directory.serializers import KsoSerializer
from budger.directory.serializers import KsoDepartment1WithHeadSerializer

from .models import BacklogEntity
from budger.directory.serializers import EntityShortSerializer, KsoEmployeeShortSerializer
from budger.directory.models.kso import KsoEmployee
from budger.directory.models.entity import Entity


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('key',)


class UserSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()

    def get_permissions(self, obj):
        return [] if obj.is_superuser else obj.get_all_permissions()

    class Meta:
        model = User
        fields = ('id', 'email', 'permissions', 'is_superuser')


class KsoEmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    kso = KsoSerializer()
    department1 = KsoDepartment1WithHeadSerializer()

    class Meta:
        model = KsoEmployee
        fields = '__all__'


class BacklogEntitySerializer(serializers.ModelSerializer):
    entity = EntityShortSerializer()
    employee = KsoEmployeeShortSerializer()

    def to_internal_value(self, data):
        internal_data = {}

        if data.get('entity'):
            obj = Entity.objects.get(pk=data['entity'])
            internal_data['entity'] = obj

        if data.get('employee'):
            obj = KsoEmployee.objects.get(pk=data['employee'])
            internal_data['employee'] = obj

        return internal_data

    class Meta:
        model = BacklogEntity
        fields = ('id', 'entity', 'employee', 'memo',)
