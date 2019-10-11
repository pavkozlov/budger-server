from django.urls import path
from .views import (
    EntityListView, EntityRetrieveView,
    KsoListView, KsoRetrieveView,
    KsoEmployeeListView, KsoEmployeeRetrieveView
)


urlpatterns = [
    path('entity', EntityListView.as_view()),
    path('entity/<int:pk>', EntityRetrieveView.as_view()),

    path('kso', KsoListView.as_view()),
    path('kso/<int:pk>', KsoRetrieveView.as_view()),

    path('kso-employee', KsoEmployeeListView.as_view()),
    path('kso-employee/<int:pk>', KsoEmployeeRetrieveView.as_view()),
]
