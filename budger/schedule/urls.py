from django.urls import include, path
from .views import EventViewSet, EnumsApiView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('', EventViewSet)

urlpatterns = [
    path('event', include(router.urls)),
    path('_enums', EnumsApiView.as_view()),
]
