from rest_framework import views, viewsets, status
from rest_framework.response import Response
from .models import (
    Event, Workflow,
    ANNUAL_STATUS_ENUM,

    EVENT_STATUS_ENUM,
    EVENT_TYPE_ENUM,
    EVENT_INITIATOR_ENUM,
    EVENT_MODE_ENUM,

    EVENT_STATUS_IN_WORK,
    EVENT_STATUS_APPROVED,
    EVENT_STATUS_DRAFT,

    WORKFLOW_STATUS_IN_WORK,
    WORKFLOW_STATUS_REJECTED
)
from .serializers import EventSerializer, WorkflowQuerySerializer
from .permissions import (
    PERM_MANAGE_EVENT,
    CanCreateEvent, CanRetrieveEvent, CanUpdateEvent, CanDeleteEvent
)

from budger.libs.shortcuts import get_object_or_none
from .filters import WorkflowFilter


class EventViewSet(viewsets.ModelViewSet):
    """
    ViewSet имеет три разрешения:
        - manage_event
        - approve_event
        - use_event
    """
    serializer_class = EventSerializer
    paginator = None
    permission_classes = [CanCreateEvent | CanRetrieveEvent | CanUpdateEvent | CanDeleteEvent]
    queryset = Event.objects.all()


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
    ViewSet для Workflow.
    """
    serializer_class = WorkflowQuerySerializer
    filter_backends = [WorkflowFilter]
    queryset = Workflow.objects.all()

    def update(self, request, *args, **kwargs):
        response = super(WorkflowViewSet, self).update(request, *args, **kwargs)

        if (
            response.status_code == 200 and
            self.get_object().status == WORKFLOW_STATUS_REJECTED
        ):
            event = self.get_object().event
            event.status = EVENT_STATUS_DRAFT
            event.save()

        return response
