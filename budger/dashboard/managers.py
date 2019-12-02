from django.db import models


class JobManager(models.Manager):
    def get_queryset(self):
        print('asd')
        return super().get_queryset().using('jobs')
