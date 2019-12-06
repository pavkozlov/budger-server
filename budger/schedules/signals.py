from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Event, Workflow, WORKFLOW_STATUS_ACCEPTED, EVENT_STATUS_APPROVED


@receiver(post_save, sender=Workflow)
def create_next_workflow_link(sender, instance, *args, **kwargs):
    if instance:

        if instance.recipient.is_head():
            if instance.status == WORKFLOW_STATUS_ACCEPTED:
                # Мероприятие согласовано
                instance.event.status = EVENT_STATUS_APPROVED
                instance.event.save()

        else:
            next_link_model = instance.get_next_link_model()
            if next_link_model:
                next_link_model.save()
