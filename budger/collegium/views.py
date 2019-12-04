from rest_framework import viewsets, permissions, response, status
from .models import Meeting, Speaker, COLLEGIUM_STATUS_APPROVED
from .serializers import MeetingSerializer
from .permission import CanApproveMeeting, CanViewMeeting
from .filters import MeetingFilter
from budger.libs.input_decorator import input_must_have
from budger.directory.models.kso import KsoEmployee


class MeetingViewSet(viewsets.ModelViewSet):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer
    filter_backends = [MeetingFilter]

    def get_permissions(self):
        if self.request.method == 'PUT' and self.request.data.get('status', None) == COLLEGIUM_STATUS_APPROVED:
            self.permission_classes = [CanApproveMeeting]

        elif self.request.method in permissions.SAFE_METHODS:
            self.permission_classes = [CanViewMeeting]

        return super(MeetingViewSet, self).get_permissions()

    @input_must_have('exec_date')
    def create(self, request, *args, **kwargs):
        meeting, _ = Meeting.objects.get_or_create(exec_date=request.data['exec_date'])
        speakers = request.data.get('speakers', [])

        for speaker in speakers:
            try:
                employee = KsoEmployee.objects.get(id=speaker['employee'])
                Speaker.objects.get_or_create(meeting=meeting, employee=employee, subjects=speaker['subjects'])
            except KsoEmployee.DoesNotExist:
                return response.Response(
                    'Не найден пользователь с id {}'.format(speaker['employee']),
                    status=status.HTTP_400_BAD_REQUEST
                )

        return response.Response(MeetingSerializer(meeting).data)

    def update(self, request, *args, **kwargs):
        try:
            meeting = Meeting.objects.get(id=kwargs['pk'])
            meeting.speakers.all().delete()
        except Meeting.DoesNotExist:
            return response.Response(
                'Не найдено мероприятие с id {}'.format(kwargs['pk']),
                status=status.HTTP_400_BAD_REQUEST
            )

        new_exec_date = request.data.get('exec_date', None)
        meetings = Meeting.objects.filter(exec_date=new_exec_date)
        if meetings.exists() and meetings.first() != meeting:
            return response.Response('Дата проведения должна быть уникальной', status=status.HTTP_400_BAD_REQUEST)

        new_speakers = request.data.get('speakers', [])
        for speaker in new_speakers:
            try:
                employee = KsoEmployee.objects.get(id=speaker['employee'])
                Speaker.objects.create(meeting=meeting, employee=employee, subjects=speaker['subjects'])
            except KsoEmployee.DoesNotExist:
                return response.Response(
                    'Не найден пользователь с id {}'.format(speaker['employee']),
                    status=status.HTTP_400_BAD_REQUEST
                )

        return super(MeetingViewSet, self).update(request, *args, **kwargs)
