from rest_framework import views, viewsets, response, generics
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
from .serializers import EventFullSerializer, WorkflowSerializer, WorkflowQuerySerializer
from budger.directory.models.kso import KsoEmployee
from django.shortcuts import get_object_or_404
from budger.libs.input_decorator import input_must_have


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventFullSerializer
    queryset = Event.objects.all()


class EnumsApiView(views.APIView):
    """
    GET Список констант
    """

    def get(self, request):
        return response.Response({
            'ANNUAL_STATUS_ENUM': ANNUAL_STATUS_ENUM,
            'EVENT_STATUS_ENUM': EVENT_STATUS_ENUM,
            'EVENT_TYPE_ENUM': EVENT_TYPE_ENUM,
            'EVENT_INITIATOR_ENUM': EVENT_INITIATOR_ENUM,
            'EVENT_MODE_ENUM': EVENT_MODE_ENUM,
        })


class WorkflowView(views.APIView):
    """
    POST Создать запись в workflow
    """

    @input_must_have(['employee_id', 'event_id', 'outcome'])
    def post(self, request):
        # Получить данные
        employee_id = request.data['employee_id']
        event_id = request.data['event_id']
        status = int(request.data['outcome'])
        memo = request.data.get('memo', None)

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


class WorkflowQueryListView(generics.ListAPIView):
    """
    GET Получить список Workflow для указанного пользователя
    """
    serializer_class = WorkflowQuerySerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        queryset = Workflow.objects.filter(recipient_id=pk).order_by('event_id', '-created').distinct('event_id')
        return queryset
