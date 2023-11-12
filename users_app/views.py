import random
import string

from django.conf import settings
from post_office import mail
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from IsMemory.helpers.CustomModelViewSet import CustomModelViewSet
from users_app.models import CustomUser
from users_app.serializers.user_serialzers import UserSerializer, UserRetrieveSerializer, UserCreateSerializer


class UserViewSet(CustomModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    serializer_list = {
        'retrieve': UserRetrieveSerializer,
        'create': UserCreateSerializer,
    }
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def reset_password(self, request, pk=None):
        user = self.get_object()
        email = request.data.get('email')
        new_password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))
        user.set_unusable_password()
        user.save()
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
        return Response({}, status=status.HTTP_200_OK)
