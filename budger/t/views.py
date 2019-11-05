from rest_framework import viewsets
from .models import Event, Department
from .serializers import EventSerializer, DepartmentSerializer
from .permissions import (
    CanListDepartment,
    CanAddDepartment,
)


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()


class DepartmentViewSet(viewsets.ModelViewSet):
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()
    permission_classes = [CanListDepartment | CanAddDepartment]
