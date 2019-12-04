from django.urls import path
from .views import (
    EntityListView, EntityRetrieveView,
    KsoListView, KsoRetrieveView,
    KsoEmployeeListView, KsoEmployeeRetrieveUpdateView, KsoEmployeeUploadPhotoView,
    EntitySubordinatesView,
    KsoResponsiblesView,
    EntityRegionalsView, EntityMunicipalsView,
    EmployeeSuperiorsView,
    EnumsView,
    KsoEmployeeListCsv
)

urlpatterns = [
    path('_enums/', EnumsView.as_view()),

    path('entity/', EntityListView.as_view()),
    path('entity/<int:pk>/', EntityRetrieveView.as_view()),

    # Дерево объектов контроля
    path('entity/regionals/', EntityRegionalsView.as_view()),
    path('entity/municipals/', EntityMunicipalsView.as_view()),
    path('entity/<int:pk>/subordinates/', EntitySubordinatesView.as_view()),

    path('kso/', KsoListView.as_view()),
    path('kso/<int:pk>/', KsoRetrieveView.as_view()),
    path('kso/responsibles/', KsoResponsiblesView.as_view()),

    path('kso-employee/', KsoEmployeeListView.as_view()),
    path('kso-employee/list_csv/', KsoEmployeeListCsv.as_view()),
    path('kso-employee/<int:pk>/', KsoEmployeeRetrieveUpdateView.as_view()),
    path('kso-employee/<int:pk>/photo/', KsoEmployeeUploadPhotoView.as_view()),
    path('kso-employee/<int:pk>/superiors/', EmployeeSuperiorsView.as_view()),
]
