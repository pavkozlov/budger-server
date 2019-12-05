from django.urls import path, include
from .views import MeetingViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('meeting', MeetingViewSet, basename='Meeting')

urlpatterns = [
    path('', include(router.urls)),
]
