from rest_framework import filters
from .models import COLLEGIUM_STATUS_DRAFT


class MeetingFilter(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        if request.user.has_perm('collegium.can_approve_meeting') or request.user.is_superuser:
            return queryset.all()
        return queryset.exclude(status=COLLEGIUM_STATUS_DRAFT)
