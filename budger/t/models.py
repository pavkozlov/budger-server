from django.db import models


class Event(models.Model):
    title = models.CharField(max_length=100)

    responsible_department = models.ForeignKey(
        'Department',
        related_name='owned_events',
        on_delete=models.DO_NOTHING,
    )

    attendant_departments = models.ManyToManyField(
        'Department',
        related_name='participated_events',
        blank=True
    )


class Department(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title
