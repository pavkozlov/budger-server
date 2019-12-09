from rest_framework import filters
from django.db.models import Q


class EntityFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        qs = queryset.all()
        if request.query_params.get('_filter__title'):
            qs = qs.filter(
                title_search__icontains=request.query_params.get('_filter__title')
            )

        if request.query_params.get('_filter__inn'):
            qs = qs.filter(
                inn__contains=request.query_params.get('_filter__inn')
            )

        if request.query_params.get('_complex_filter_1'):
            term = request.query_params.get('_complex_filter_1')
            qs = qs.filter(
                Q(title_search__icontains=term) |
                Q(inn__contains=term) |
                Q(ogrn__contains=term) |
                Q(head_name__icontains=term)
            )

        return qs


class KsoEmployeeFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        qs = queryset

        if request.query_params.get('kso_id') is not None:
            qs = qs.filter(
                kso__id=request.query_params.get('kso_id')
            )

        if request.query_params.get('_filter__kso_id') is not None:
            qs = qs.filter(
                kso__id=request.query_params.get('_filter__kso_id')
            )

        if request.query_params.get('_filter__name') is not None:
            qs = qs.filter(
                name__icontains=request.query_params.get('_filter__name')
            )

        return qs
