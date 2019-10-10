from django.urls import path
from .views import (
    EntityListView, EntityRetrieveView,
    KsoListView, KsoRetrieveView
)


urlpatterns = [
    path('entity', EntityListView.as_view()),
    path('entity/<int:pk>', EntityRetrieveView.as_view()),
    path('kso', KsoListView.as_view()),
    path('kso/<int:pk>', KsoRetrieveView.as_view()),
]
