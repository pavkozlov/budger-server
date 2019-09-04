from rest_framework import routers, serializers, viewsets
from records.serializers import UserSerializer, RecordSerializer, TagSerializer
from django.contrib.auth.models import User
from records.models import Record, Tag


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# ViewSets define the view behavior.
class RecordViewSet(viewsets.ModelViewSet):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer


# ViewSets define the view behavior.
class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
