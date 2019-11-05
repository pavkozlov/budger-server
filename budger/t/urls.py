from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, DepartmentViewSet


router1 = DefaultRouter()
router1.register('', EventViewSet)

router2 = DefaultRouter()
router2.register('', DepartmentViewSet)

urlpatterns = [
    path('events/', include(router1.urls)),
    path('departments/', include(router2.urls)),
]
