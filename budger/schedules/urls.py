from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, EnumsApiView, WorkflowListCreateView

router = DefaultRouter()
router.register('', EventViewSet, basename='Event')

urlpatterns = [
    path('events/', include(router.urls)),
    path('_enums/', EnumsApiView.as_view()),
    path('workflows/', WorkflowListCreateView.as_view()),
]
