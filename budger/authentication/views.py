from rest_framework import views, generics, viewsets
from django.contrib.auth.models import User, AnonymousUser, update_last_login
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND
from rest_framework.response import Response
from budger.directory.models.kso import KsoEmployee
from .serializers import TokenSerializer, UserSerializer, KsoEmployeeSerializer as _KsoEmployeeSerializer
from budger.directory.serializers import KsoEmployeeSerializer
from .permissions import CanViewUser, CanUpdateUser, IsOwner
from .models import BacklogEntity
from .serializers import BacklogEntitySerializer
from django.shortcuts import get_object_or_404


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
            user = User.objects.get(email__icontains=email)
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


class UserRetrieveView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [CanViewUser]


class UserPasswordUpdateView(views.APIView):
    """
    PUT     Сохранение пароля пользователя.
            Отдельный эндпойнт (без CRUD) реализаван потому, что все эти действия выполняются в рамках работы
            с employee.
    """
    permission_classes = [CanUpdateUser]

    def put(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        password = request.data.get('password')

        if user_id is None or password is None:
            return Response(status=HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, pk=user_id)
        user.set_password(password)
        user.save()

        return Response(status=HTTP_204_NO_CONTENT)


class EmployeeView(views.APIView):
    """
    GET     Сведения о текущем работнике.
    """

    def _get_employee(self, request):
        auth_user = request.user

        if auth_user is not None and type(auth_user) is not AnonymousUser:
            try:
                employee = KsoEmployee.objects.get(user=auth_user)
                return employee
            except KsoEmployee.DoesNotExist:
                pass

        return None

    def get(self, request):
        employee = self._get_employee(request)
        if employee is not None:
            return Response(
                {'user': _KsoEmployeeSerializer(employee).data}
            )
        else:
            return Response(status=HTTP_403_FORBIDDEN)


class CurrentUserView(generics.RetrieveAPIView):
    """
    GET     Сведения о текущем пользователе.
    """

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        if user is None or type(user) is AnonymousUser:
            return Response(status=HTTP_404_NOT_FOUND)
        else:
            employee = user.ksoemployee
            if employee is not None:
                return Response({
                    'user': UserSerializer(user).data,
                    'employee': KsoEmployeeSerializer(employee).data,
                    'superiors': KsoEmployeeSerializer(employee.get_superiors(), many=True).data,
                })


class BacklogEntityViewset(viewsets.ModelViewSet):
    """
    ViewSet для EntityBacklog.
    """
    serializer_class = BacklogEntitySerializer
    permission_classes = [IsOwner, ]

    def get_queryset(self):
        return BacklogEntity.objects.filter(employee=self.request.user.ksoemployee)