from django.urls import path
from .views import RecordListCreateView, RecordDetailView, RecordFilterView


urlpatterns = [
    path('records/', RecordListCreateView.as_view(), name="records-list-create"),
    path('records/filter/', RecordFilterView.as_view(), name="records-filter"),
    path('records/<int:pk>/', RecordDetailView.as_view(), name="records-detail"),
]
