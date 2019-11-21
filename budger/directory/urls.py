from django.urls import path
from .views import (
    EntityListView, EntityRetrieveView,
    KsoListView, KsoRetrieveView,
    KsoEmployeeListView, KsoEmployeeRetrieveView,
    EntitySubordinatesView,
    KsoResponsiblesView,
    EntityRegionalsView, EntityMunicipalsView,
    EmployeeSuperiorsView
)

urlpatterns = [
    path('entity', EntityListView.as_view()),
    path('entity/<int:pk>', EntityRetrieveView.as_view()),

    # Дерево объектов контроля
    path('entity/regionals/', EntityRegionalsView.as_view()),
    path('entity/municipals/', EntityMunicipalsView.as_view()),
    path('entity/<int:pk>/subordinates/', EntitySubordinatesView.as_view()),

    path('kso', KsoListView.as_view()),
    path('kso/<int:pk>', KsoRetrieveView.as_view()),
    path('kso/responsibles', KsoResponsiblesView.as_view()),

    path('kso-employee', KsoEmployeeListView.as_view()),
    path('kso-employee/<int:pk>', KsoEmployeeRetrieveView.as_view()),
    path('kso-employee/<int:pk>/superiors/', EmployeeSuperiorsView.as_view()),
]
