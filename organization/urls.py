from django.urls import path
from .views import OrganizationCommonListView, OrganizationCommonRetrieveView


urlpatterns = [
    path('organization/', OrganizationCommonListView.as_view()),
    path('organization/<int:pk>/', OrganizationCommonRetrieveView.as_view()),
]
