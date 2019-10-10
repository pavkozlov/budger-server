from rest_framework import views, generics
from django.contrib.auth.models import User as AuthUser, AnonymousUser
from .models import User
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny

from rest_framework.status import (
    HTTP_403_FORBIDDEN,
    HTTP_400_BAD_REQUEST
)
from rest_framework.response import Response
from .serializers import UserSerializer, TokenSerializer


class LoginView(views.APIView):
    """
    POST Вход пользователя в систему
        @email
        @password
    """
    permission_classes = (AllowAny,)

    @staticmethod
    def authenticate(email, password):
        """ Authenticate user by email/passwords and return User if okay and None if not okay. """
        try:
            auth_user = AuthUser.objects.get(email=email)
            if auth_user.check_password(password):
                return auth_user
        except AuthUser.DoesNotExist:
            pass

        return None

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if email is None or password is None:
            return Response(
                {'error': 'email-and-password-required'},
                status=HTTP_400_BAD_REQUEST
            )

        auth_user = self.authenticate(email, password)

        if not auth_user:
            return Response({'error': 'invalid-credentials'})

        try:
            user = User.objects.get(auth_user=auth_user)
        except User.DoesNotExist:
            return Response({'error': 'user-does-not-exist'})

        token, _ = Token.objects.get_or_create(user=auth_user)

        return Response({
            'token': TokenSerializer(token).data,
            'user': UserSerializer(user).data
        })


class LogoutView(views.APIView):
    """
    POST Выход пользователя из системы.
    """
    def post(self, request):
        request.user.auth_token.delete()
        return Response()


class UserView(views.APIView):
    """
    GET Сведения о текущем пользователе.
    POST Сохранение данных текущего пользователя:
        @last_name
        @first_name
        @second_name
        @position
    """
    def get_user(self, request):
        auth_user = request.user

        if auth_user is not None and type(auth_user) is not AnonymousUser:
            try:
                return User.objects.get(auth_user=auth_user)
            except User.DoesNotExist:
                pass

        return None

    def get(self, request):
        user = self.get_user(request)

        if user:
            return Response(
                {'user': UserSerializer(user).data}
            )
        else:
            return Response(status=HTTP_403_FORBIDDEN)

    def post(self, request):
        user = self.get_user(request)

        if user and 'user' in request.data:
            user_data = request.data['user']
            user.last_name = user_data.get('last_name', '')
            user.first_name = user_data.get('first_name', '')
            user.second_name = user_data.get('second_name', '')
            user.position = user_data.get('position', '')
            user.save()

        return Response(
            {'user': UserSerializer(user).data}
        )
