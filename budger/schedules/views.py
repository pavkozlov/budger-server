from rest_framework import views, viewsets, status
from rest_framework.response import Response
from .models import (
    Event, Workflow,
    ANNUAL_STATUS_ENUM,
    EVENT_STATUS_ENUM,
    EVENT_TYPE_ENUM,
    EVENT_INITIATOR_ENUM,
    EVENT_MODE_ENUM,
    EVENT_STATUS_APPROVED
)
from .serializers import EventSerializer, WorkflowQuerySerializer
from .permissions import (
    CanCreateEvent,
    CanRetrieveEvent,
    CanUpdateEvent,
    CanDeleteEvent
)

from .filters import WorkflowFilter
from .renderers import EsgfkXmlRenderer


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
    queryset = Event.objects.filter(status=EVENT_STATUS_APPROVED).order_by('group', 'exec_from', 'responsible_department')


class WorkflowViewSet(viewsets.ModelViewSet):
    """
    ViewSet для Workflow.
    """
    serializer_class = WorkflowQuerySerializer
    filter_backends = [WorkflowFilter]
    queryset = Workflow.objects.all()


class EsgfkXmlView(views.APIView):
    """
    Выгрузка XML для ЕИС ГФК.
    @year - год, за который необходимо выгружать данные
    """
    renderer_classes = [EsgfkXmlRenderer]

    def get(self, request):
        events = Event.objects.all()
        return Response(
            events,
            headers={'Content-Disposition': 'attachment; filename="export-for-esgfk.xml"'}
        )
