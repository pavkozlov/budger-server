from django.urls import path
from .views import NatProjectsView, RegProjectsView, AggregationView


urlpatterns = [
    path('natprojects/', NatProjectsView.as_view()),
    path('regprojects/', RegProjectsView.as_view()),
    path('regprojects/<str:pk>/', RegProjectsView.as_view()),
    path('aggregation/', AggregationView.as_view()),
]
