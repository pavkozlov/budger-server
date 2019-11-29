from rest_framework import filters


class WorkflowsFilter(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        employee_filter = request.query_params.get('_filter__recipient_id', None)

        if employee_filter:
            return queryset.filter(recipient_id=employee_filter).order_by('event_id', '-created').distinct('event_id')

        return queryset.all()
