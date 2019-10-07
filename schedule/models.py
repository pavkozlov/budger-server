from django.db import models
from organization.models.organization_common import OrganizationCommon


SCHEDULE_STATUS = [
    (1, 'В работе'),
    (2, 'На согласовании'),
    (3, 'Согласовано'),
]


class Schedule(models.Model):
    year = models.SmallIntegerField(db_index=True)
    status = models.SmallIntegerField(db_index=True, choices=SCHEDULE_STATUS)

    def __str__(self):
        return '{} - {}'.format(self.year, self.status)

    class Meta:
        ordering = ['-year']


class Event(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    organization = models.ForeignKey(OrganizationCommon, on_delete=models.CASCADE)

    revision_from = models.DateField()
    revision_to = models.DateField()
    period_from = models.DateField()
    period_to = models.DateField()
    status = models.SmallIntegerField(db_index=True, choices=SCHEDULE_STATUS)

    def __str__(self):
        return '{} - {}'.format(self.revision_from, self.revision_to)

    class Meta:
        ordering = ['-revision_from']
