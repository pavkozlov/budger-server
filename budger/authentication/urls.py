from django.urls import path, include
from .views import (
    EmployeeView,
    CurrentUserView,
    LoginView,
    LogoutView,
    UserRetrieveView,
    UserPasswordUpdateView,
    BacklogEntityViewset
)
from rest_framework import routers

router = routers.SimpleRouter()
router.register('', BacklogEntityViewset, basename='EntityBacklog')
urlpatterns = router.urls

urlpatterns = [
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('employee', EmployeeView.as_view()),
    path('current_user/', CurrentUserView.as_view()),
    path('users/<int:pk>/', UserRetrieveView.as_view()),
    path('users/<int:pk>/password/', UserPasswordUpdateView.as_view()),
    path('backlogentity/', include(router.urls)),
]
