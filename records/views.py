from rest_framework import generics
from records.serializers import RecordSerializer, TokenSerializer
from django.contrib.auth.models import User
from records.models import Record, Tag
from .decorators import validate_request_data
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework import permissions
from django.contrib.auth import authenticate, login
from rest_framework_jwt.settings import api_settings


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


"""
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
"""


class RecordListCreateView(generics.ListCreateAPIView):
    """
    GET records/
    POST records/
    """
    queryset = Record.objects.all()
    serializer_class = RecordSerializer

    @validate_request_data
    def post(self, request, *args, **kwargs):
        record = Record.objects.create(
            title=request.data['title'],
            description=request.data['description'],
            amount=request.data['amount'],
            user=request.user
        )

        record.tags.set(Tag.objects.filter(id__in=[1, 2]))

        return Response(
            data=RecordSerializer(record).data,
            status=status.HTTP_201_CREATED
        )


class RecordDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET songs/:id/
    PUT songs/:id/
    DELETE songs/:id/
    """
    queryset = Record.objects.all()
    serializer_class = RecordSerializer

    def get(self, request, *args, **kwargs):
        try:
            record = self.queryset.get(pk=kwargs['pk'])
            return Response(RecordSerializer(record).data)
        except Record.DoesNotExist:
            return Response(
                data={
                    'message': 'Record with id {} does not exist'.format(kwargs['pk'])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    @validate_request_data
    def put(self, request, *args, **kwargs):
        try:
            record = self.queryset.get(pk=kwargs['pk'])
            serializer = RecordSerializer()
            updated_song = serializer.update(record, request.data)
            return Response(RecordSerializer(updated_song).data)
        except Record.DoesNotExist:
            return Response(
                data={
                    'message': 'Record with id {} does not exist'.format(kwargs['pk'])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            record = self.queryset.get(pk=kwargs["pk"])
            record.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Record.DoesNotExist:
            return Response(
                data={
                    'message': "Record with id: {} does not exist".format(kwargs['pk'])
                },
                status=status.HTTP_404_NOT_FOUND
            )


class LoginView(generics.CreateAPIView):
    """
    POST auth/login/
    """
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # login saves the user’s ID in the session,
            # using Django’s session framework.
            login(request, user)
            serializer = TokenSerializer(data={
                # using drf jwt utility functions to generate a token
                'token': jwt_encode_handler(jwt_payload_handler(user))
            })
            serializer.is_valid()
            print(serializer.data)
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
