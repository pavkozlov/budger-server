from rest_framework import views, viewsets, status
from rest_framework.response import Response
from .models import (
    ANNUAL_STATUS_ENUM,
    EVENT_STATUS_ENUM,
    EVENT_TYPE_ENUM,
    EVENT_INITIATOR_ENUM,
    EVENT_MODE_ENUM,
    Event, Workflow,
    EVENT_STATUS_IN_WORK,
    EVENT_STATUS_APPROVED,
    EVENT_STATUS_DRAFT,
    WORKFLOW_STATUS_IN_WORK
)
from .serializers import EventSerializer, WorkflowQuerySerializer
from budger.directory.models.kso import KsoEmployee
from .permissions import (
    PERM_MANAGE_EVENT,
    PERM_MANAGE_WORKFLOW
)

from budger.libs.shortcuts import get_object_or_none


class EventViewSet(viewsets.ModelViewSet):
    """
    ViewSet имеет три разрешения:
        - manage_event
        - approve_event
        - use_event
    """
    serializer_class = EventSerializer

    def get_queryset(self):
        qs = Event.objects.exclude(status=EVENT_STATUS_DRAFT)
        u = self.request.user

        if u.has_perm(PERM_MANAGE_EVENT):
            qs = qs | Event.objects.all()

        return qs

    def create(self, request, *args, **kwargs):
        u = self.request.user

        if u.has_perm(PERM_MANAGE_EVENT):
            return super(EventViewSet, self).create(request, *args, **kwargs)

        return Response(status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        u = self.request.user
        event = self.get_object()

        if event.status == EVENT_STATUS_DRAFT and not u.has_perm(PERM_MANAGE_EVENT):
            return Response(status=status.HTTP_403_FORBIDDEN)

        # if event.status == EVENT_STATUS_IN_WORK and not u.has_perm(PERM_APPROVE_EVENT):
        #    return Response(status=status.HTTP_403_FORBIDDEN)

        if event.status == EVENT_STATUS_APPROVED and not u.is_superuser:
            return Response(status=status.HTTP_403_FORBIDDEN)

        if event.status == EVENT_STATUS_DRAFT and request.data.get('status') == EVENT_STATUS_IN_WORK and event.author == request.user.ksoemployee:
            # Если автор event изменил статус с DRAFT на IN_WORK, автоматически создать согласование
            # TODO: Вынести это в сигналы.
            if not event.author.is_head():
                # Create first workflow.
                # Get recipient
                sender = event.author
                superiors = sender.get_superiors()
                recipient = get_object_or_none(KsoEmployee, pk=superiors[0]['id'])
                if recipient is not None:
                    Workflow.objects.create(
                        event=event,
                        sender=sender,
                        recipient=recipient,
                        status=WORKFLOW_STATUS_IN_WORK
                    )

        return super(EventViewSet, self).update(request, *args, **kwargs)


class EnumsApiView(views.APIView):
    """
    GET Список констант
    """

    def get(self, request):
        return Response({
            'ANNUAL_STATUS_ENUM': ANNUAL_STATUS_ENUM,
            'EVENT_STATUS_ENUM': EVENT_STATUS_ENUM,
            'EVENT_TYPE_ENUM': EVENT_TYPE_ENUM,
            'EVENT_INITIATOR_ENUM': EVENT_INITIATOR_ENUM,
            'EVENT_MODE_ENUM': EVENT_MODE_ENUM,
        })


class WorkflowViewSet(viewsets.ModelViewSet):
    """
    ViewSet для Workflow
    При отсутствии PERM_VIEWALL_WORKFLOW и PERM_MANAGEALL_WORKFLOW операции производятся только с согласованиями,
    направленными непосредственно пользователю.
    """
    serializer_class = WorkflowQuerySerializer

    def get_queryset(self):
        u = self.request.user

        if u.has_perm(PERM_MANAGE_WORKFLOW):
            return Workflow.objects.all()

        return Workflow.objects.filter(
            recipient=u.ksoemployee
        )
