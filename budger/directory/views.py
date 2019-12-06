"""
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
"""

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

import os
from django.shortcuts import get_object_or_404
from rest_framework import generics, filters, response, views, parsers, status
from django.db.models import Q
from budger.libs.dynamic_fields import DynaFieldsListAPIView
from budger.libs.pagination import UnlimitedResultsSetPagination
import budger.app_settings as app_settings
from .models.entity import Entity, MunicipalBudget, SPEC_EVENT_CODE_ENUM
from .models.kso import Kso, KsoEmployee, KsoDepartment1
from .permissions import CanUpdateEmployee

from .serializers import (
    EntitySubordinatesSerializer, EntityListSerializer, EntitySerializer,
    KsoListSerializer, KsoSerializer,
    KsoEmployeeListSerializer,
    KsoEmployeeSerializer,
    KsoDepartment1ShortSerializer, KsoDepartment2ShortSerializer,
    MunicipalBudgetSerializer,
    KsoDepartment1WithHeadSerializer
)

from .filters import EntityFilter
from .renderers import KsoEmployeeCsvRenderer


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
    filter_backends = [filters.SearchFilter]
    search_fields = ['title_search']
    paginator = None


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
        queryset = KsoEmployee.objects.filter(is_developer=False)

        kso_filter = self.request.query_params.get('kso_id')  # TODO: remove it
        if kso_filter is not None:
            queryset = queryset.filter(kso__id=kso_filter)

        kso_filter = self.request.query_params.get('_filter__kso_id')
        if kso_filter is not None:
            queryset = queryset.filter(kso__id=kso_filter)

        name_filter = self.request.query_params.get('_filter__name')
        if name_filter is not None:
            queryset = queryset.filter(name__icontains=name_filter)

        return queryset.order_by('name')


class KsoEmployeeListCsv(DynaFieldsListAPIView):
    """
    GET Список всех сотрудников КСО, отрендеренные в csv
    """
    serializer_class = KsoEmployeeListSerializer
    renderer_classes = [KsoEmployeeCsvRenderer, ]
    queryset = KsoEmployee.objects.filter(is_developer=False)


class KsoEmployeeRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    """
    GET Сведения о выбранном сотруднике КСО
    PUT Обновление данных выбранного сотрудника КСО
    """
    serializer_class = KsoEmployeeSerializer
    queryset = KsoEmployee.objects.all()
    permission_classes = [CanUpdateEmployee]


class KsoEmployeeUploadPhotoView(views.APIView):
    """
    PUT Загрузить файл с фото работника. Обязателен заголовок Content-Disposition:inline;filename={photo.jpg}
    """
    parser_classes = (parsers.FileUploadParser,)
    permission_classes = [CanUpdateEmployee]

    def put(self, request, *args, **kwargs):
        response_status = status.HTTP_400_BAD_REQUEST
        employee_id = kwargs.get('pk')

        if employee_id is not None:
            employee = get_object_or_404(KsoEmployee, pk=employee_id)
            photo_file = request.FILES['file']

            if photo_file.content_type.lower() in ('image/jpeg', 'image/png'):
                # Prepare to save image
                path = app_settings.EMPLOYEE_PHOTO_DIR

                name = 'employee_{}'.format(employee_id)
                if photo_file.content_type.lower() == 'image/jpeg':
                    name += '.jpg'
                if photo_file.content_type.lower() == 'image/png':
                    name += '.png'

                # Save image
                with open(os.path.join(path, name), 'wb') as file:
                    file.write(photo_file.read())

                # Update Employee model
                employee.photo_slug = name
                employee.save()

                response_status = status.HTTP_204_NO_CONTENT

        return response.Response(status=response_status)


class KsoResponsiblesView(views.APIView):
    """
    GET Список подразделений КСО, могущих являться отвестсвенными за мероприятия
    """

    def get(self, request):
        kso = request.user.ksoemployee.kso
        departments = KsoDepartment1.objects.filter(kso=kso, can_participate_in_events=True)
        data = KsoDepartment1WithHeadSerializer(departments, many=True).data

        return response.Response({'departments': data})


class EntityRegionalsView(views.APIView):
    """
    GET Список муниципальных объектов контроля - ГРБС.
    @_filter__title__inn Фильтр по названию и ИНН.
    """

    def get(self, request):
        terms = request.query_params.get('_filter__title__inn', None)

        if terms is not None:
            queryset = Entity.objects.filter(
                (Q(title_search__icontains=terms) | Q(inn=terms)) &
                Q(budget_lvl_code__in=['20', '50'])
            )
        else:
            queryset = Entity.objects.filter(
                parent_id__isnull=True,
                opf_code__in=['75201', '75203', '75204'],
                org_type_code__in=['01', '02'],
                budget_lvl_code__in=['20', '50'],
                org_status_code__in=['1', '4'],
            )

        data = EntitySubordinatesSerializer(queryset, many=True).data
        return response.Response(data)


class EntityMunicipalsView(views.APIView):
    """
    GET Список групп верхнего уровня муниципальных объектов контроля.
    @_filter__budget_code Список муниципальных объектов контроля с заданным budget_code.
    @_filter__title__inn Фильтр по названию и ИНН.
    """

    def get(self, request):
        terms_budget = request.query_params.get('_filter__budget_code', None)
        terms_title = request.query_params.get('_filter__title__inn', None)

        if terms_budget is not None:
            parent = get_object_or_404(MunicipalBudget, code=terms_budget)
            queryset = Entity.objects.filter(pk__in=parent.subordinates)
            data = EntitySubordinatesSerializer(queryset, many=True).data

        elif terms_title is not None:
            queryset = Entity.objects.filter(
                (Q(title_search__icontains=terms_title) | Q(inn=terms_title)) &
                Q(budget_lvl_code__in=['31', '32'])
            )
            data = EntitySubordinatesSerializer(queryset, many=True).data

        else:
            queryset = MunicipalBudget.objects.all()
            data = MunicipalBudgetSerializer(queryset, many=True).data

        return response.Response(data)


class EntitySubordinatesView(views.APIView):
    """
    GET Список муниципальных объектов контроля - ГРБС.
    """

    def get(self, request, pk):
        parent = get_object_or_404(Entity, pk=pk)
        queryset = Entity.objects.filter(pk__in=parent.subordinates)
        data = EntitySubordinatesSerializer(queryset, many=True).data
        return response.Response(data)


class EmployeeSuperiorsView(views.APIView):
    def get_employee(self, employee):
        data = {
            'id': employee.id,
            'name': employee.name,
            'position': employee.position,
        }

        if employee.department1 is not None:
            data['ksodepartment1'] = KsoDepartment1ShortSerializer(employee.department1).data

        if employee.department2 is not None:
            data['ksodepartment2'] = KsoDepartment2ShortSerializer(employee.department2).data

        return data

    def get_head(self, department):
        if department is not None:
            department_head = department.head
            return self.get_employee(department_head)

    def get(self, request, pk):
        data = []

        employee = get_object_or_404(KsoEmployee, id=pk)
        kso_head = employee.kso.head

        if employee != kso_head:

            dep2_head = self.get_head(employee.department2)
            if dep2_head:
                data.append(dep2_head)

            dep1_head = self.get_head(employee.department1)
            if dep1_head:
                data.append(dep1_head)

            data.append(self.get_employee(kso_head))

        return response.Response(data)


class EnumsView(views.APIView):
    """
    GET Список констант
    """

    def get(self, request):
        return response.Response({
            'SPEC_EVENT_CODE_ENUM': SPEC_EVENT_CODE_ENUM
        })
