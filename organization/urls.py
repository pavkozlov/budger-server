from django.urls import path
from .views import OrganizationCommonView


urlpatterns = [
    path('organization/', OrganizationCommonView.as_view()),
    # path('records/<int:pk>/', RecordDetailView.as_view(), name="records-detail"),
]
