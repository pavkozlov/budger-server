from rest_framework import views
from django.contrib.auth.models import User as AuthUser, AnonymousUser
from .models import User
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_403_FORBIDDEN,
    HTTP_200_OK
)
from rest_framework.response import Response
from .serializers import UserSerializer, TokenSerializer


class LoginView(views.APIView):
    """
    POST Вход пользователя в систему
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
                {'error': 'Please provide both email and password.'},
                status=HTTP_400_BAD_REQUEST
            )

        auth_user = self.authenticate(email, password)

        if not auth_user:
            return Response(
                {'error': 'Invalid Credentials.'},
                status=HTTP_404_NOT_FOUND
            )

        user = User.objects.get(auth_user=auth_user)

        if not user:
            return Response(
                {'error': 'User object is not found for given auth user.'},
                status=HTTP_404_NOT_FOUND
            )

        token, _ = Token.objects.get_or_create(user=auth_user)

        return Response(
            {
                'token': TokenSerializer(token).data,
                'user': UserSerializer(user).data
            },
            status=HTTP_200_OK
        )


class LogoutView(views.APIView):
    """
    POST Выход пользователя из системы
    """
    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=HTTP_200_OK)


class UserView(views.APIView):
    """
    GET Сведения о текущем пользователе
    """
    def get(self, request):
        auth_user = request.user

        # Guard
        if auth_user is None or type(auth_user) is AnonymousUser:
            return Response(status=HTTP_403_FORBIDDEN)

        # Core user is okay
        user = User.objects.get(auth_user=auth_user)

        return Response(
            {'user': UserSerializer(user).data},
            status=HTTP_200_OK
        )
