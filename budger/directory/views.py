"""
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
"""

from django.shortcuts import get_object_or_404
from rest_framework import generics, filters, response, views
from budger.directory.models.entity import Entity, MunicipalBudget
from budger.directory.models.kso import Kso, KsoEmployee, KsoDepartment1, KsoDepartment2
from budger.libs.dynamic_fields import DynaFieldsListAPIView
from budger.libs.pagination import UnlimitedResultsSetPagination

from .serializers import (
    EntitySubordinatesSerializer, EntityListSerializer, EntitySerializer,
    KsoListSerializer, KsoSerializer,
    KsoEmployeeListSerializer,
    KsoEmployeeMediumSerializer,
    KsoEmployeeShortSerializer,
    KsoDepartment1ShortSerializer, KsoDepartment2ShortSerializer,
    MunicipalBudgetSerializer
)

from .filters import EntityFilter
from django.db.models import Q


class EntityListView(DynaFieldsListAPIView):
    """
    GET Список объектов контроля.
    @_filter__title
    @_filter__inn
    """
    serializer_class = EntityListSerializer
    filter_backends = [EntityFilter]
    queryset = Entity.objects.all()

    """
    @method_decorator(cache_page(60 * 60 * 2))
    def list(self, request):
        return super().list(request)
    """


class EntityRetrieveView(generics.RetrieveAPIView):
    """
    GET Сведения об объекте контроля.
    """
    serializer_class = EntitySerializer
    queryset = Entity.objects.all()


class KsoListView(DynaFieldsListAPIView):
    """
    GET Список КСО.
    """
    serializer_class = KsoListSerializer
    queryset = Kso.objects.all()
    pagination_class = UnlimitedResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['title_search']


class KsoRetrieveView(generics.RetrieveAPIView):
    """
    GET Сведения о выбранном КСО.
    """
    serializer_class = KsoSerializer
    queryset = Kso.objects.all()


class KsoEmployeeListView(DynaFieldsListAPIView):
    """
    GET Список сотрудников КСО.
    @_filter__kso_id - фильтр по полю kso.id
    """
    serializer_class = KsoEmployeeListSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        queryset = KsoEmployee.objects.order_by('name')

        kso_id = self.request.query_params.get('kso_id', None)
        if kso_id is not None:
            queryset = queryset.filter(kso__id=kso_id).order_by('name')

        return queryset


class KsoEmployeeRetrieveView(generics.RetrieveAPIView):
    """
    GET Сведения о выбранном сотруднике КСО
    """
    serializer_class = KsoEmployeeMediumSerializer
    queryset = KsoEmployee.objects.all()


class KsoResponsiblesView(views.APIView):
    """
    GET Список сотрудников и подразделений КСО, могущих являться отвестсвенными за мероприятия
    """

    def get(self, request):
        kso = request.user.ksoemployee.kso

        employees = KsoEmployee.objects.filter(kso=kso, can_be_responsible=True)
        departments = KsoDepartment1.objects.filter(kso=kso, can_participate_in_events=True)

        return response.Response({
            'departments': KsoDepartment1ShortSerializer(departments, many=True).data,
            'employees': KsoEmployeeShortSerializer(employees, many=True).data
        })


class EntityRegionalsView(views.APIView):
    """
    GET Список муниципальных объектов контроля - ГРБС.
    """

    def get(self, request):
        if 'filter' in request.query_params and request.query_params['filter']:
            terms = request.query_params['filter']
            queryset = Entity.objects.filter(
                (Q(title_search__icontains=terms) | Q(inn=terms)) &
                Q(budget_lvl_code__in=['20', '50'])
            )
            serializer = EntitySubordinatesSerializer(queryset, many=True)
        else:
            queryset = Entity.objects.filter(
                parent_id__isnull=True,
                opf_code__in=['75201', '75203', '75204'],
                org_type_code__in=['01', '02'],
                budget_lvl_code__in=['20', '50'],
                org_status_code__in=['1', '4'],
            )
            serializer = EntitySubordinatesSerializer(queryset, many=True)
        return response.Response(serializer.data)


class EntityMunicipalsView(views.APIView):
    """
    GET Список групп верхнего уровня муниципальных объектов контроля.
    @code -- Список муниципальных объектов контроля с заданным budget_code
    """

    def get(self, request):
        if 'budget_code' in request.query_params and request.query_params['budget_code']:
            budget_code = request.query_params['budget_code']
            parent = get_object_or_404(MunicipalBudget, code=budget_code)
            queryset = Entity.objects.filter(pk__in=parent.subordinates)
            serializer = EntitySubordinatesSerializer(queryset, many=True)
        elif 'filter' in request.query_params and request.query_params['filter']:
            terms = request.query_params['filter']
            queryset = Entity.objects.filter(
                (Q(title_search__icontains=terms) | Q(inn=terms)) &
                Q(budget_lvl_code__in=['31', '32'])
            )
            serializer = EntitySubordinatesSerializer(queryset, many=True)
        else:
            queryset = MunicipalBudget.objects.all()
            serializer = MunicipalBudgetSerializer(queryset, many=True)
        return response.Response(serializer.data)


class EntitySubordinatesView(views.APIView):
    """
    GET Список муниципальных объектов контроля - ГРБС.
    """

    def get(self, request, pk):
        parent = get_object_or_404(Entity, pk=pk)
        queryset = Entity.objects.filter(pk__in=parent.subordinates)
        serializer = EntitySubordinatesSerializer(queryset, many=True)
        return response.Response(serializer.data)


class EmployeeSuperiorsView(views.APIView):
    def get_employee(self, employee):
        data = {
            'name': employee.name,
            'position': employee.position,
        }

        if employee.department1 is not None:
            data['ksodepartment1'] = KsoDepartment1ShortSerializer(employee.department1).data

        if employee.department2 is not None:
            data['ksodepartment2'] = KsoDepartment2ShortSerializer(employee.department2).data

        return data

    def append_departments_heads(self, employee, result):
        if employee.department2 is not None:
            department = employee.department2
            department_head = department.head
            result.append(self.get_employee(department_head))

        if employee.department1 is not None:
            department = employee.department1
            department_head = department.head
            result.append(self.get_employee(department_head))

    def get(self, request, pk):
        result = []

        employee = KsoEmployee.objects.get(user_id=pk)
        kso_head = employee.kso.head

        result.append(self.get_employee(kso_head))

        if employee == kso_head:
            return response.Response(result)

        self.append_departments_heads(employee, result)

        result.append(self.get_employee(employee))

        return response.Response(result)
