from django.urls import path
from .views import (
    OrganizationListView, OrganizationRetrieveView,
    OrganizationKsoListView, OrganizationKsoRetrieveView
)


urlpatterns = [
    path('organization/', OrganizationListView.as_view()),
    path('organization/<int:pk>/', OrganizationRetrieveView.as_view()),
    path('organization_kso/', OrganizationKsoListView.as_view()),
    path('organization_kso/<int:pk>/', OrganizationKsoRetrieveView.as_view()),
]
