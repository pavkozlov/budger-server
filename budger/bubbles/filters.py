from rest_framework import filters
from budger.libs.shortcuts import can_be_int


class AggregationFilter(filters.BaseFilterBackend):
    @staticmethod
    def _param(request, param_code):
        return request.query_params.get(f'_filter__{param_code}')

    def filter_queryset(self, request, queryset, view):
        if self._param(request, 'year') is not None:
            y = self._param(request, 'year')
            years = y.split(',') if ',' in y else [y]
            queryset = queryset.filter(
                year__in=[int(i) for i in years]
            )

        if self._param(request, 'regproj_participant') is not None:
            queryset = queryset.filter(regproj_participant=True)

        if self._param(request, 'budget_amount_plan') is not None:
            param = self._param(request, 'budget_amount_plan')
            if can_be_int(param):
                queryset = queryset.filter(budget_amount_plan__gte=param)

        if self._param(request, 'budget_amount_fact') is not None:
            param = self._param(request, 'budget_amount_fact')
            if can_be_int(param):
                queryset = queryset.filter(budget_amount_fact__gte=param)

        if self._param(request, 'violations_count') is not None:
            param = self._param(request, 'violations_count')
            if can_be_int(param):
                queryset = queryset.filter(violations_count__gte=param)

        if self._param(request, 'violations_amount') is not None:
            param = self._param(request, 'violations_amount')
            if can_be_int(param):
                queryset = queryset.filter(violations_amount__gte=param)

        return queryset
