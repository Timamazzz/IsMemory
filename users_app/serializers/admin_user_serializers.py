from rest_framework import serializers

from users_app.models import CustomUser


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class AdminUserRetrieveSerializer(AdminUserSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'patronymic', 'email']


class AdminUserResetPasswordSerializer(AdminUserSerializer):
    class Meta:
        model = CustomUser
        fields = ['email']
