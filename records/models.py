from django.db import models
from django.contrib.auth.models import User


class Record(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    amount = models.FloatField()
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    # Keys
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField("Tag")

    def __str__(self):
        return "{} - {}".format(self.created, self.title)

    class Meta:
        ordering = ["-created"]


class Tag(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title
