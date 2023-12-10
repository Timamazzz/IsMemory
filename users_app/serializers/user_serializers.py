from rest_framework import serializers

from users_app.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class UserCreateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True, label='Имя')
    last_name = serializers.CharField(required=True, label='Фамилия')
    patronymic = serializers.CharField(required=True, label='Отчество')
    email = serializers.EmailField(required=True, label='Электронная почта')
    phone_number = serializers.CharField(required=True, label='Номер телефона')
    password = serializers.CharField(required=True, write_only=True, label='Пароль')

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'patronymic', 'email', 'phone_number', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserRetrieveSerializer(UserSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'patronymic', 'email', 'phone_number']


class UserResetPasswordSerializer(UserSerializer):
    class Meta:
        model = CustomUser
        fields = ['email']
