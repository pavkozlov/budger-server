from django.urls import path
from .views import (
    EmployeeView,
    CurrentUserView,
    LoginView,
    LogoutView,
    UserRetrieveView,
    UserPasswordUpdateView
)


urlpatterns = [
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('employee', EmployeeView.as_view()),
    path('current_user/', CurrentUserView.as_view()),
    path('users/<int:pk>/', UserRetrieveView.as_view()),
    path('users/<int:pk>/password/', UserPasswordUpdateView.as_view()),
]
