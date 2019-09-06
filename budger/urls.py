from django.contrib import admin
from django.urls import path, include, re_path
from .views import login, user

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login', login),
    path('api/user', user),
    re_path(r'api/', include('records.urls')),
]
