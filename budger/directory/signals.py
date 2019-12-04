from django.db.models.signals import post_save
from django.dispatch import receiver
from .models.kso import KsoEmployee


@receiver(post_save, sender=KsoEmployee)
def update_user_with_employee(sender, instance, *args, **kwargs):
    if instance and instance.user is not None and instance.user.email is not None:
        user = instance.user
        user.email = instance.email.lower()
        user.username = user.email.split('@')[0].lower()
        user.save()
