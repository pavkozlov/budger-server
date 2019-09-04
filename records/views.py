from rest_framework import viewsets
from records.serializers import UserSerializer, RecordSerializer, TagSerializer, RecordSerializerListItem
from django.contrib.auth.models import User
from records.models import Record, Tag
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RecordViewSet(viewsets.ModelViewSet):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer


class RecordList(viewsets.ViewSet):
    permission_classes = []

    def list(self, request):
        queryset = Record.objects.all()
        serializer = RecordSerializerListItem(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Record.objects.all()
        record = get_object_or_404(queryset, pk=pk)
        serializer = RecordSerializer(record)
        return Response(serializer.data)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
