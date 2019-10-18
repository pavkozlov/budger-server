from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, EnumsApiView


router = DefaultRouter()
router.register('', EventViewSet)

urlpatterns = [
    path('events/', include(router.urls)),
    path('_enums/', EnumsApiView.as_view()),
]