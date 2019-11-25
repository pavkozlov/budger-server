from rest_framework import views, viewsets, response
from .models import (
    ANNUAL_STATUS_ENUM,
    EVENT_MODE_ENUM,
    EVENT_TYPE_ENUM,
    EVENT_INITIATOR_ENUM,
    Event
)
from .serializers import EventFullSerializer


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventFullSerializer
    queryset = Event.objects.all()


class EnumsApiView(views.APIView):
    def get(self, request):
        return response.Response({
            'ANNUAL_STATUS_ENUM': ANNUAL_STATUS_ENUM,
            'EVENT_MODE_ENUM': EVENT_MODE_ENUM,
            'EVENT_TYPE_ENUM': EVENT_TYPE_ENUM,
            'EVENT_INITIATOR_ENUM': EVENT_INITIATOR_ENUM
        })
