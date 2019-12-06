from rest_framework import filters
from django.db.models import Q


class EntityFilter(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        if request.query_params.get('_filter__title'):
            term = request.query_params.get('_filter__title')
            return queryset.filter(title_search__icontains=term)

        if request.query_params.get('_filter__inn'):
            term = request.query_params.get('_filter__inn')
            return queryset.filter(inn__contains=term)

        if request.query_params.get('_complex_filter_1'):
            term = request.query_params.get('_complex_filter_1')
            return queryset.filter(
                Q(title_search__icontains=term) |
                Q(inn__contains=term) |
                Q(ogrn__contains=term) |
                Q(head_name__icontains=term)
            )

        return queryset.all()
