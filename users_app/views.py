import secrets

from django.conf import settings
from post_office import mail
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users_app.admin_permissions import HasDashboardAdminGroupPermission
from IsMemory.helpers.CustomModelViewSet import CustomModelViewSet
from users_app.models import CustomUser
from users_app.serializers.admin_user_serializers import AdminUserSerializer, AdminUserRetrieveSerializer, \
    AdminUserResetPasswordSerializer
from users_app.serializers.user_serializers import UserResetPasswordSerializer, UserRetrieveSerializer, \
    UserCreateSerializer, UserPartialUpdateSerializer


@api_view(['POST'])
def reset_password(request):
    if request.method == 'POST':
        email = request.data.get('email')

        try:
            user = CustomUser.objects.get(email=email)
            new_password = secrets.token_urlsafe(8)

            user.set_unusable_password()
            user.set_password(new_password)
            user.save()

            subject = 'Сброс пароля'
            message = f'Ваш новый пароль: {new_password}'
            html_message = f'Ваш новый пароль: {new_password}'

            mail.send(
                email,
                settings.DEFAULT_FROM_EMAIL,
                subject=subject,
                message=message,
                html_message=html_message,
                priority='now'
            )

            return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User with such email not found'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'Invalid request method'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({
                'user': serializer.data,
                'access': access_token,
                'refresh': str(refresh),
                'message': 'User registered successfully'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Invalid request method'}, status=status.HTTP_400_BAD_REQUEST)


class AdminViewSet(CustomModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = AdminUserSerializer
    serializer_list = {
        'retrieve': AdminUserRetrieveSerializer,
        'reset-password': AdminUserResetPasswordSerializer,
    }
    permission_classes = [permissions.IsAuthenticated]


class UserViewSet(CustomModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = AdminUserSerializer
    serializer_list = {
        'retrieve': UserRetrieveSerializer,
        'create': UserCreateSerializer,
        'reset-password': UserResetPasswordSerializer,
        'update': UserPartialUpdateSerializer,
    }
