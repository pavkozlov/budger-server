from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from records.views import UserViewSet, RecordViewSet, TagViewSet, RecordList

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'api/users', UserViewSet)
router.register(r'api/records', RecordViewSet)
router.register(r'api/recs', RecordList, basename='record')
router.register(r'api/tags', TagViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('admin/', admin.site.urls),    
    path(r'', include(router.urls)),
    path(r'api/', include('rest_framework.urls', namespace='rest_framework'))
]
