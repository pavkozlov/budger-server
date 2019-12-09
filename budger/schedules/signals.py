from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import (
    Event, Workflow,
    WORKFLOW_STATUS_ACCEPTED, WORKFLOW_STATUS_IN_WORK,
    EVENT_STATUS_APPROVED, EVENT_STATUS_IN_WORK
)


@receiver(post_save, sender=Event)
def create_first_workflow_link(sender, instance, *args, **kwargs):
    """ Если мероприятие изменило статус на IN_WORK, а список согласований пуст, создать первое согласование """
    if instance and instance.status == EVENT_STATUS_IN_WORK and kwargs.get('created') is False:
        workflows = Workflow.objects.filter(event=instance)
        if not workflows and not instance.author.is_head():
            superiors = instance.author.get_superiors()
            Workflow.objects.create(
                event=instance,
                sender=instance.author,
                recipient=superiors[0],
                status=WORKFLOW_STATUS_IN_WORK
            )


@receiver(post_save, sender=Workflow)
def create_next_workflow_link(sender, instance, *args, **kwargs):
    """ При изменении статуса workflow создать следующий workflow. """
    if instance and kwargs.get('created') is False:

        if instance.recipient.is_head() and instance.status == WORKFLOW_STATUS_ACCEPTED:
            # Мероприятие согласовано
            event = instance.event
            event.status = EVENT_STATUS_APPROVED
            event.save()

        else:
            next_link_model = instance.get_next_link_model()
            if next_link_model:
                next_link_model.save()
