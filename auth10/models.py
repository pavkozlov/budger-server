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

    def __str__(self):
        return '{} {} {} ({})'.format(
            self.last_name,
            self.first_name,
            self.second_name,
            self.auth_user
        )
