from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, EnumsApiView, WorkflowViewSet, EsgfkXmlView

router = DefaultRouter()
router.register('events', EventViewSet, basename='Event')
router.register('workflows', WorkflowViewSet, basename='Workflow')

urlpatterns = [
    path('_enums/', EnumsApiView.as_view()),
    path('eisgfk-xml/', EsgfkXmlView.as_view()),
    path('', include(router.urls)),
]
