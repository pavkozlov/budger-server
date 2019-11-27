from rest_framework import views, viewsets, response
from .models import (
    ANNUAL_STATUS_ENUM,
    EVENT_STATUS_ENUM,
    EVENT_TYPE_ENUM,
    EVENT_INITIATOR_ENUM,
    EVENT_MODE_ENUM,
    Event, Workflow,
    EVENT_STATUS_IN_WORK,
    EVENT_STATUS_ACCEPTED,
    WORKFLOW_STATUS_REJECTED,
    WORKFLOW_STATUS_ACCEPTED,
)
from .serializers import EventFullSerializer, WorkflowSerializer
from budger.directory.models.kso import KsoEmployee
from django.shortcuts import get_object_or_404
from rest_framework.status import HTTP_400_BAD_REQUEST


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventFullSerializer
    queryset = Event.objects.all()


class EnumsApiView(views.APIView):
    def get(self, request):
        return response.Response({
            'ANNUAL_STATUS_ENUM': ANNUAL_STATUS_ENUM,
            'EVENT_STATUS_ENUM': EVENT_STATUS_ENUM,
            'EVENT_TYPE_ENUM': EVENT_TYPE_ENUM,
            'EVENT_INITIATOR_ENUM': EVENT_INITIATOR_ENUM,
            'EVENT_MODE_ENUM': EVENT_MODE_ENUM,
        })


class WorkflowView(views.APIView):
    def post(self, request):
        # Получить данные
        employee_id = request.data.get('employee_id', None)
        event_id = request.data.get('event_id', None)
        status = int(request.data.get('outcome', None))
        memo = request.data.get('memo', None)

        if employee_id is None or event_id is None:
            return response.Response(status=HTTP_400_BAD_REQUEST)

        if status not in (WORKFLOW_STATUS_ACCEPTED, WORKFLOW_STATUS_REJECTED):
            return response.Response(status=HTTP_400_BAD_REQUEST)

        if status == WORKFLOW_STATUS_REJECTED and memo is None:
            return response.Response(status=HTTP_400_BAD_REQUEST)

        sender = get_object_or_404(KsoEmployee, id=employee_id)
        event = get_object_or_404(Event, id=event_id)

        # Получить список начальников
        superiors = sender.get_superiors()

        # Если аудиторов больше 1, отправляем на согласование председателю
        if event.responsible_employees.count() > 1:
            recipient_id = superiors[-1]['id']
            recipient = KsoEmployee.objects.get(id=recipient_id)
            event_status = EVENT_STATUS_IN_WORK
        else:
            if sender.is_head():
                # Если отправитель глава КСО, статус = согласовано
                recipient = sender
                event_status = EVENT_STATUS_ACCEPTED
            else:
                # Если отправитель не глава КСО, получатель = ближайший руководитель
                recipient_id = superiors[1]['id']
                recipient = KsoEmployee.objects.get(id=recipient_id)
                event_status = EVENT_STATUS_IN_WORK

        # Создать запись в Workflow
        workflow = Workflow.objects.create(
            event=event,
            sender=sender,
            recipient=recipient,
            status=status,
            memo=memo
        )

        # Обновить статус мероприятия
        event.status = event_status
        event.save()

        return response.Response(WorkflowSerializer(workflow).data)
