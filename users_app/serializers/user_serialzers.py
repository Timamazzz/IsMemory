from rest_framework import serializers

from users_app.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class UserCreateSerializer(UserSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'first_name', 'last_name', 'patronymic']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserRetrieveSerializer(UserSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'patronymic', 'email']
