from django.contrib.auth.models import User as AuthUser
from django.db import models
from organization.models.employee import Employee


class User(models.Model):
    auth_user = models.OneToOneField(AuthUser, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, null=True, on_delete=models.CASCADE)
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    second_name = models.CharField(max_length=30, null=True)
    position = models.CharField(max_length=100)

    read_only_fields = (auth_user, employee)

    def __str__(self):
        return '{} {} {} ({})'.format(
            self.last_name,
            self.first_name,
            self.second_name,
            self.auth_user
        )

    def create(self, validated_data):
        user = User(
            last_name=validated_data['last_name'],
            first_name=validated_data['first_name'],
            second_name=validated_data['second_name'],
            position=validated_data['position'],
        )
        user.save()
        return user

    def update(self, user, validated_data):
        user.last_name = validated_data.get('last_name', user.last_name)
        return user
