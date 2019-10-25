from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth10/', include('budger.authentication.urls')),
    path('api/directory/', include('budger.directory.urls')),
    path('api/schedules/', include('budger.schedules.urls')),
    path('api/t/', include('budger.t.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
