from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth10/', include('budger.authentication.urls')),
    path('api/directory/', include('budger.directory.urls')),
    path('api/schedules/', include('budger.schedules.urls')),
    path('api/t/', include('budger.t.urls')),
]
