from rest_framework import filters
from .models import Workflow
from .permissions import PERM_MANAGE_WORKFLOW


class WorkflowFilter(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        qs = queryset

        if request.query_params.get('_filter__status'):
            qs = qs.filter(status=request.query_params.get('_filter__status'))

        if request.query_params.get('_filter__event'):
            qs = qs.filter(event_id=request.query_params.get('_filter__event'))

        return qs
