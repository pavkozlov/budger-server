from rest_framework import filters
from django.db.models import Q
from budger.libs.shortcuts import can_be_int, normalize_search_str
from .models.entity import EntityGroup


class EntityFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):

        if request.query_params.get('_filter__title'):
            term = request.query_params.get('_filter__title')
            queryset = queryset.filter(
                title_search__icontains=normalize_search_str(term)
            )

        if request.query_params.get('_filter__inn'):
            queryset = queryset.filter(
                inn__contains=request.query_params.get('_filter__inn')
            )

        if request.query_params.get('_filter__opf'):
            queryset = queryset.filter(
                opf_code__in=request.query_params['_filter__opf'].split(',')
            )

        if request.query_params.get('_filter__1'):
            term = request.query_params.get('_filter__1')
            normal_term = normalize_search_str(term)
            queryset = queryset.filter(
                Q(title_search__icontains=normal_term) |
                Q(head_name__icontains=normal_term) |
                Q(inn__contains=term) |
                Q(ogrn__contains=term)
            )

        if request.query_params.get('_filter__group') == 'municipals':
            group = EntityGroup.objects.get(code='municipals')
            queryset = queryset.filter(id__in=group.data)

        if request.query_params.get('_filter__group') == 'regionals':
            group = EntityGroup.objects.get(code='regionals')
            queryset = queryset.filter(id__in=group.data)

        return queryset


class KsoEmployeeFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        qs = queryset

        p = request.query_params.get('kso_id')
        if can_be_int(p):
            qs = qs.filter(kso=p)

        p = request.query_params.get('_filter__kso_id')
        if can_be_int(p):
            qs = qs.filter(kso=p)

        if request.query_params.get('_filter__name') is not None:
            qs = qs.filter(
                name__icontains=request.query_params.get('_filter__name')
            )

        return qs
