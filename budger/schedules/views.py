from rest_framework import views, viewsets, response
from .models import (
    ANNUAL_STATUS_ENUM,
    EVENT_STATUS_ENUM,
    EVENT_TYPE_ENUM,
    EVENT_INITIATOR_ENUM,
    EVENT_MODE_ENUM,
    Event, Workflow,
    EVENT_STATUS_SENT,
    EVENT_STATUS_AGREED_BY_DEPARTMENT1_HEAD,
    EVENT_STATUS_AGREED_BY_DEPARTMENT2_HEAD,
    EVENT_STATUS_AGREED_BY_KSO_HEAD,
    WORKFLOW_STATUS_ACCEPTED, WORKFLOW_STATUS_REJECTED
)
from .serializers import EventFullSerializer, WorkFlowSerializer
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
    def get(self, request):
        # Получить данные
        employee_id = request.data.get('employee_id', None)
        event_id = request.data.get('event_id', None)
        mode = request.data.get('mode', None)
        memo = request.data.get('memo', None)

        # Проверить данные
        if employee_id is None or event_id is None:
            return response.Response(status=HTTP_400_BAD_REQUEST)

        if mode not in ('accepted', 'rejected'):
            return response.Response(status=HTTP_400_BAD_REQUEST)

        if mode == 'rejected' and memo is None:
            return response.Response(status=HTTP_400_BAD_REQUEST)

        employee = get_object_or_404(KsoEmployee, id=employee_id)
        event = get_object_or_404(Event, id=event_id)

        # Получить статус WorkFlow
        if mode == 'accepted':
            workflow_status = WORKFLOW_STATUS_ACCEPTED
        elif mode == 'rejected':
            workflow_status = WORKFLOW_STATUS_REJECTED

        # Получить список начальников
        superiors = employee.get_superiors()

        # Получить статус мероприятия и получателя
        if len(superiors) == 1:
            # Пользователь является председателем КСО
            recipient = employee
            status = EVENT_STATUS_AGREED_BY_KSO_HEAD

        elif len(superiors) > 1:
            recipient_id = superiors[1]['id']
            recipient = KsoEmployee.objects.get(id=recipient_id)

            if len(superiors) == 2:
                # Пользователь является начальником департамента
                if workflow_status == WORKFLOW_STATUS_ACCEPTED:
                    status = EVENT_STATUS_AGREED_BY_DEPARTMENT1_HEAD
                elif workflow_status == WORKFLOW_STATUS_REJECTED:
                    status = EVENT_STATUS_AGREED_BY_DEPARTMENT2_HEAD

            if len(superiors) == 3:
                # Пользователь является начальником отдела
                if workflow_status == WORKFLOW_STATUS_ACCEPTED:
                    status = EVENT_STATUS_AGREED_BY_DEPARTMENT2_HEAD
                elif workflow_status == WORKFLOW_STATUS_REJECTED:
                    status = EVENT_STATUS_SENT

            if len(superiors) == 4:
                # Пользователь является рядовым сотрудником
                status = EVENT_STATUS_SENT

        event.status = status
        event.save()

        workflow = Workflow.objects.create(event=event,
                                           sender=employee,
                                           recipient=recipient,
                                           status=workflow_status,
                                           memo=memo)

        return response.Response(WorkFlowSerializer(workflow).data)
