from rest_framework import views
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User, AnonymousUser, update_last_login
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT
from rest_framework.response import Response
from budger.directory.models.kso import KsoEmployee
from .serializers import TokenSerializer, KsoEmployeeSerializer
from .permissions import CanUpdateUser


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
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
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

        user = self.authenticate(email, password)

        if not user:
            return Response({'error': 'invalid-credentials'})

        try:
            kso_employee = KsoEmployee.objects.get(user=user)
        except KsoEmployee.DoesNotExist:
            return Response({'error': 'user-does-not-have-employee-relation'})

        token, _ = Token.objects.get_or_create(user=user)
        update_last_login(None, user)

        return Response({
            'token': TokenSerializer(token).data,
            'employee': KsoEmployeeSerializer(kso_employee).data
        })


class LogoutView(views.APIView):
    """
    POST    Выход пользователя из системы.
    """

    def post(self, request):
        request.user.auth_token.delete()
        return Response()


class UserPasswordUpdateView(views.APIView):
    """
    PUT     Сохранение пароля пользователя.
            Отдельный эндпойнт (без CRUD) реализаван потому, что все эти действия выполняются в рамках работы
            с employee.
    """
    permission_classes = [CanUpdateUser]

    def put(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user_password = request.data.get('password')
        if user_id is not None and user_password is not None:
            user = get_object_or_404(User, pk=user_id)
            user.set_password(user_password)
            return Response(status=HTTP_204_NO_CONTENT)

        return Response(status=HTTP_400_BAD_REQUEST)


class EmployeeView(views.APIView):
    """
    GET     Сведения о текущем работнике.

    POST    Сохранение данных текущего работника:
            @last_name
            @first_name
            @second_name
            @position
    """

    def get_user(self, request):
        auth_user = request.user

        if auth_user is not None and type(auth_user) is not AnonymousUser:
            try:
                return KsoEmployee.objects.get(user=auth_user)
            except KsoEmployee.DoesNotExist:
                pass

        return None

    def get(self, request):
        user = self.get_user(request)
        if user:
            return Response(
                {'user': KsoEmployeeSerializer(user).data}
            )
        else:
            return Response(status=HTTP_403_FORBIDDEN)
