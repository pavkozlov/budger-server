from django.urls import path
from .views import JobListView, KsoImportExportView


urlpatterns = [
    path('jobs/', JobListView.as_view()),
    path('kso/', KsoImportExportView.as_view()),
]
