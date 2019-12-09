from rest_framework import filters
from budger.libs.shortcuts import can_be_int


class WorkflowFilter(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        qs = queryset

        p = request.query_params.get('_filter__recipient')
        if can_be_int(p):
            qs = qs.filter(recipient=p)

        p = request.query_params.get('_filter__status')
        if can_be_int(p):
            qs = qs.filter(status=p)

        p = request.query_params.get('_filter__event')
        if can_be_int(p):
            qs = qs.filter(event_id=p)

        return qs
