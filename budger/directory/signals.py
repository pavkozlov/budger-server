from django.db.models.signals import post_save
from django.dispatch import receiver
from .models.kso import KsoEmployee
from django.contrib.auth.models import User


@receiver(post_save, sender=KsoEmployee)
def create_related_profile(sender, instance, created, *args, **kwargs):
    if instance and created:
        a = 1
