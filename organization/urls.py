from django.urls import path
from .views import OrganizationCommonListView, OrganizationCommonRetrieveView, OrganizationKsoView


urlpatterns = [
    path('organization/', OrganizationCommonListView.as_view()),
    path('organization/<int:pk>/', OrganizationCommonRetrieveView.as_view()),
    path('organization_kso/', OrganizationKsoView.as_view()),
    path('organization_kso/<int:pk>/', OrganizationKsoView.as_view()),
]
