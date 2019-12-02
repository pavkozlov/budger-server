from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import JobViewSet


router = DefaultRouter()
router.register('', JobViewSet)


urlpatterns = [
    path('jobs/', include(router.urls)),
]
