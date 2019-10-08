from django.urls import path
from .views import OrganizationListView, OrganizationRetrieveView, OrganizationKsoView


urlpatterns = [
    path('organization/', OrganizationListView.as_view()),
    path('organization/<int:pk>/', OrganizationRetrieveView.as_view()),
    path('organization_kso/', OrganizationKsoView.as_view()),
    path('organization_kso/<int:pk>/', OrganizationKsoView.as_view()),
]
