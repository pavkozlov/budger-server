from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, EnumsApiView, WorkflowView, WorkflowQueryListView

router = DefaultRouter()
router.register('', EventViewSet)

urlpatterns = [
    path('events/', include(router.urls)),
    path('_enums/', EnumsApiView.as_view()),
    path('workflow_create/', WorkflowView.as_view()),
    path('workflow_query/<pk>', WorkflowQueryListView.as_view())
]
