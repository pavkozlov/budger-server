from rest_framework import views, viewsets, response, generics, status
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
from .serializers import EventSerializer, WorkflowSerializer, WorkflowQuerySerializer
from budger.directory.models.kso import KsoEmployee
from django.shortcuts import get_object_or_404
from budger.libs.input_decorator import input_must_have
from .permissions import (
    PERM_USE_EVENT,
    PERM_APPROVE_EVENT,
    PERM_MANAGE_EVENT,
    PERM_VIEWALL_WORKFLOW
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
        u = self.request.user
        qs = Event.objects.none()

        if u.has_perm(PERM_MANAGE_EVENT):
            qsa = Event.objects.filter(status=EVENT_STATUS_DRAFT)
            qs = qs | qsa

        if u.has_perm(PERM_APPROVE_EVENT):
            qsa = Event.objects.filter(status=EVENT_STATUS_IN_WORK)
            qs = qs | qsa

        if u.has_perm(PERM_USE_EVENT):
            qsa = Event.objects.filter(status=EVENT_STATUS_APPROVED)
            qs = qs | qsa

        return qs

    def create(self, request, *args, **kwargs):
        u = self.request.user

        if u.has_perm(PERM_MANAGE_EVENT):
            return super(EventViewSet, self).create(request, *args, **kwargs)

        return response.Response(status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        u = self.request.user
        event = self.get_object()

        if event.status == EVENT_STATUS_DRAFT and not u.has_perm(PERM_MANAGE_EVENT):
            return response.Response(status=status.HTTP_403_FORBIDDEN)

        if event.status == EVENT_STATUS_IN_WORK and not u.has_perm(PERM_APPROVE_EVENT):
            return response.Response(status=status.HTTP_403_FORBIDDEN)

        if event.status == EVENT_STATUS_APPROVED and not u.has_perm(PERM_USE_EVENT):
            return response.Response(status=status.HTTP_403_FORBIDDEN)

        if event.status == EVENT_STATUS_DRAFT and request.data.get('status') == EVENT_STATUS_IN_WORK and event.author == request.user.ksoemployee:
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
        return response.Response({
            'ANNUAL_STATUS_ENUM': ANNUAL_STATUS_ENUM,
            'EVENT_STATUS_ENUM': EVENT_STATUS_ENUM,
            'EVENT_TYPE_ENUM': EVENT_TYPE_ENUM,
            'EVENT_INITIATOR_ENUM': EVENT_INITIATOR_ENUM,
            'EVENT_MODE_ENUM': EVENT_MODE_ENUM,
        })


class WorkflowListCreateView(generics.ListCreateAPIView):
    """
    GET Получить список Workflow для указанного пользователя
    @_filter__recipient_id

    POST Создать запись в workflow
    """
    serializer_class = WorkflowQuerySerializer

    def get_queryset(self):
        u = self.request.user

        if u.has_perm(PERM_VIEWALL_WORKFLOW):
            return Workflow.objects.all()

        return Workflow.objects.filter(
            recipient=u.ksoemployee,
            status=WORKFLOW_STATUS_IN_WORK
        )

    @input_must_have(['employee_id', 'event_id', 'outcome'])
    def create(self, request, *args, **kwargs):
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
                event_status = EVENT_STATUS_APPROVED
            else:
                # Если отправитель не глава КСО, получатель = ближайший руководитель
                recipient_id = superiors[0]['id']
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

