from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, response, status

from budger.libs.input_decorator import input_must_have
from budger.libs.shortcuts import get_object_or_none
from budger.directory.models.kso import KsoEmployee

from .models import (
    Meeting,
    Speaker,
    MEETING_STATUS_DRAFT,
    MEETING_STATUS_APPROVING,
    MEETING_STATUS_PUBLISHED,
)
from .serializers import MeetingSerializer
from .permission import (
    PERM_MANAGE_MEETING,
    PERM_APPROVE_MEETING,
    PERM_VIEW_MEETING
)


class MeetingViewSet(viewsets.ModelViewSet):
    """
    ViewSet имеет три разрешения:
        manage_meeting
        approve_meeting
        view_meeting
    """
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer

    def get_queryset(self):
        u = self.request.user
        if u.has_perm(PERM_MANAGE_MEETING):
            return Meeting.objects.all()
        elif u.has_perm(PERM_APPROVE_MEETING):
            return Meeting.objects.filter(status=MEETING_STATUS_APPROVING)
        elif u.has_perm(PERM_VIEW_MEETING):
            return Meeting.objects.filter(status=MEETING_STATUS_PUBLISHED)

    @input_must_have('exec_date')
    def create(self, request, *args, **kwargs):
        u = self.request.user
        if not u.has_perm('manage_meeting'):
            return response.Response(status=status.HTTP_403_FORBIDDEN)

        # Guard: meeting date has to be unique.
        m1 = get_object_or_none(Meeting, exec_date=request.data['exec_date'])
        if m1:
            return response.Response(status=status.HTTP_400_BAD_REQUEST)

        meeting = Meeting.objects.create(exec_date=request.data['exec_date'])
        speakers = request.data.get('speakers', [])

        for s in speakers:
            employee = get_object_or_none(KsoEmployee, pk=s['employee']['id'])
            if employee:
                Speaker.objects.create(
                    meeting=meeting,
                    employee=employee,
                    subjects=s['subjects']
                )
            else:
                return response.Response(status=status.HTTP_400_BAD_REQUEST)

        return super(MeetingViewSet, self).create(request, *args, **kwargs)

    @input_must_have('exec_date')
    def update(self, request, *args, **kwargs):
        user = self.request.user
        meeting = self.get_object()

        if meeting.status == MEETING_STATUS_DRAFT and not user.has_perm('manage_meeting'):
            return response.Response(status=status.HTTP_403_FORBIDDEN)

        if meeting.status == MEETING_STATUS_APPROVING and not user.has_perm('approve_meeting'):
            return response.Response(status=status.HTTP_403_FORBIDDEN)
        
        if meeting.status == MEETING_STATUS_PUBLISHED and not user.has_perm('view_meeting'):
            return response.Response(status=status.HTTP_403_FORBIDDEN)

        # Guard: meeting date has to be unique.
        m1 = get_object_or_none(Meeting, exec_date=request.data['exec_date'])
        if m1 and m1.id != meeting.id:
            return response.Response(status=status.HTTP_400_BAD_REQUEST)

        new_speakers = request.data.get('speakers', [])

        for s in meeting.speakers.all():
            if len(new_speakers) > 0:
                ns = new_speakers.pop(0)
                s.employee = get_object_or_none(KsoEmployee, pk=ns['employee']['id'])
                s.subjects = ns['subjects']
                s.save()
            else:
                s.delete()

        if len(new_speakers) > 0:
            for s in new_speakers:
                employee = get_object_or_none(KsoEmployee, pk=s['employee']['id'])
                if employee:
                    Speaker.objects.create(
                        meeting=meeting,
                        employee=employee,
                        subjects=s['subjects']
                    )

        return super(MeetingViewSet, self).update(request, *args, **kwargs)
