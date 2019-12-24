from rest_framework import filters
from django.db.models import Q
from budger.libs.shortcuts import can_be_int
from. models import Aggregation


class AggregationFilter(filters.BaseFilterBackend):
    @staticmethod
    def _param(request, param_code):
        return request.query_params.get('_filter__{}'.format(param_code))

    def filter_queryset(self, request, queryset, view):
        """
        Для начала из агрегации выбираются только те данные, что соответствуют запросу пользователя.
        Вторым этапом мы выбираем все данные о выбранных ГРБС.
        """
        if self._param(request, 'year') is not None:
            y = self._param(request, 'year')
            years = y.split(',') if ',' in y else [y]
            queryset = queryset.filter(
                year__in=[int(i) for i in years]
            )

        if self._param(request, 'regproj_participant_true') is not None:
            queryset = queryset.filter(regproj_participant=True)

        if self._param(request, 'regproj_participant_false') is not None:
            queryset = queryset.filter(regproj_participant__isnull=True)

        if self._param(request, 'budget_amount_plan_min') is not None:
            param = self._param(request, 'budget_amount_plan_min')
            if can_be_int(param):
                queryset = queryset.filter(budget_amount_plan__gte=param)

        if self._param(request, 'budget_amount_plan_max') is not None:
            param = self._param(request, 'budget_amount_plan_max')
            if can_be_int(param):
                queryset = queryset.filter(budget_amount_plan__lte=param)

        if self._param(request, 'budget_amount_fact_min') is not None:
            param = self._param(request, 'budget_amount_fact_min')
            if can_be_int(param):
                queryset = queryset.filter(budget_amount_fact__gte=param)

        if self._param(request, 'budget_amount_fact_max') is not None:
            param = self._param(request, 'budget_amount_fact_max')
            if can_be_int(param):
                queryset = queryset.filter(budget_amount_fact__lte=param)

        if self._param(request, 'violations_false') is not None:
            queryset = queryset.filter(violations_count__isnull=True)

        if self._param(request, 'violations_count_min') is not None:
            param = self._param(request, 'violations_count_min')
            if can_be_int(param):
                queryset = queryset.filter(violations_count__gte=param)

        if self._param(request, 'violations_count_max') is not None:
            param = self._param(request, 'violations_count_max')
            if can_be_int(param):
                queryset = queryset.filter(violations_count__lte=param)

        if self._param(request, 'violations_amount_min') is not None:
            param = self._param(request, 'violations_amount_min')
            if can_be_int(param):
                queryset = queryset.filter(violations_amount__gte=param)

        if self._param(request, 'violations_amount_max') is not None:
            param = self._param(request, 'violations_amount_max')
            if can_be_int(param):
                queryset = queryset.filter(violations_amount__lte=param)

        # Тут мы имеем только те записи из bubble_aggregation, что соответствуют запросу прользователя.
        # Однако, для корректного отображения необходимо запрашивать все данные для попавших в запрос ГРБС.

        q = Q()

        for rec in queryset.distinct('year', 'entity'):
            q1 = Q(
                entity=rec.entity,
                year=rec.year,
            )
            q.add(q1, Q.OR)

        return Aggregation.objects.filter(q).order_by('entity__search_name', 'year')
