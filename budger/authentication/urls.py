from django.urls import path
from .views import (
    EmployeeView,
    LoginView,
    LogoutView
)


urlpatterns = [
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('employee', EmployeeView.as_view()),
]
