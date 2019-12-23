from django.db import models
from budger.directory.models.entity import Entity
from budger.directory.models.kso import KsoEmployee


class BacklogEntity(models.Model):
    employee = models.ForeignKey(KsoEmployee, on_delete=models.CASCADE, db_index=True)
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)
    memo = models.TextField(null=True, blank=True)
