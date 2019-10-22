from rest_framework import views
from django.contrib.auth.models import User, AnonymousUser, update_last_login
# from .models import Profile
from budger.directory.models.kso import KsoEmployee
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from .serializers import TokenSerializer, KsoEmployeeSerializer


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
    POST Выход пользователя из системы.
    """

    def post(self, request):
        request.user.auth_token.delete()
        return Response()


class EmployeeView(views.APIView):
    """
    GET Сведения о текущем работнике.
    POST Сохранение данных текущего работника:
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

    def post(self, request):
        user = self.get_user(request)

        if user and 'user' in request.data:
            user_data = request.data['user']
            user.name = user_data.get('name', '')
            user.position = user_data.get('position', '')
            user.save()

        return Response(
            {'user': KsoEmployeeSerializer(user).data}
        )
