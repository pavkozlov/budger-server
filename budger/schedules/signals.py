from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Workflow


@receiver(post_save, sender=Workflow)
def create_next_workflow_link(sender, instance, *args, **kwargs):
    if instance:
        next_link_model = instance.get_next_link_model()
        if next_link_model:
            next_link_model.save()
