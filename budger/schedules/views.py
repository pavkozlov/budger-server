from rest_framework import views, viewsets, response
from .models import (
    ANNUAL_STATUS_ENUM,
    EVENT_STATUS_ENUM,
    EVENT_TYPE_ENUM,
    EVENT_FINANCIAL_CONTROL_ENUM,
    EVENT_FORM_ENUM,
    EVENT_INITIATOR_ENUM,
    EVENT_INSPECTION_ENUM,
    EVENT_METHOD_ENUM,
    EVENT_MODE_ENUM,
    EVENT_REASON_ENUM,
    Event
)
from .serializers import EventSerializer


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()


class EnumsApiView(views.APIView):
    def get(self, request):
        return response.Response({
            'ANNUAL_STATUS_ENUM': ANNUAL_STATUS_ENUM,
            'EVENT_STATUS_ENUM': EVENT_STATUS_ENUM,
            'EVENT_TYPE_ENUM': EVENT_TYPE_ENUM,
            'EVENT_FINANCIAL_CONTROL_ENUM': EVENT_FINANCIAL_CONTROL_ENUM,
            'EVENT_FORM_ENUM': EVENT_FORM_ENUM,
            'EVENT_INITIATOR_ENUM': EVENT_INITIATOR_ENUM,
            'EVENT_INSPECTION_ENUM': EVENT_INSPECTION_ENUM,
            'EVENT_METHOD_ENUM': EVENT_METHOD_ENUM,
            'EVENT_MODE_ENUM': EVENT_MODE_ENUM,
            'EVENT_REASON_ENUM': EVENT_REASON_ENUM,
        })
