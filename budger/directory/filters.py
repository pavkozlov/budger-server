from rest_framework import filters


class EntityFilter(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        if request.query_params.get('_filter__title'):
            term = request.query_params.get('_filter__title')
            return queryset.filter(title_search__icontains=term)

        if request.query_params.get('_filter__inn'):
            term = request.query_params.get('_filter__inn')
            return queryset.filter(inn__contains=term)

        return queryset.all()
