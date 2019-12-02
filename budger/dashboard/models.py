from django.db import models
from .managers import JobManager


JOB_STATUS_ENUM = [
    (1, 'success'),
    (2, 'warning'),
    (3, 'error'),
]


class Job(models.Model):
    objects = JobManager

    id = models.BigAutoField(primary_key=True, editable=False)
    code = models.CharField(max_length=300, db_index=True)
    uuid = models.CharField(max_length=300, unique=True)
    status = models.PositiveSmallIntegerField(choices=JOB_STATUS_ENUM)
    created = models.DateTimeField()
    description = models.CharField(max_length=2000, null=True, blank=True)

    class Meta:
        db_table = 'jobs_log'
        ordering = ['-created']
        permissions = [('dashboard.can_view_jobs', 'Can view jobs list.')]

    def __str__(self):
        return '{} - {}'.format(self.created, self.code,)
