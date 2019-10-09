from django.urls import path
from .views import (
    UserView,
    LoginView,
    LogoutView
)


urlpatterns = [
    path('auth10/login', LoginView.as_view()),
    path('auth10/logout', LogoutView.as_view()),
    path('auth10/user', UserView.as_view()),
]
