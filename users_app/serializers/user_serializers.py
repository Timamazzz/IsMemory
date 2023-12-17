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


class UserPartialUpdateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True, label='Имя')
    last_name = serializers.CharField(required=True, label='Фамилия')
    patronymic = serializers.CharField(required=True, label='Отчество')
    email = serializers.EmailField(required=True, label='Электронная почта')
    phone_number = serializers.CharField(required=True, label='Номер телефона')
    password = serializers.CharField(required=True, write_only=True, label='Новый пароль')
    password_confirmation = serializers.CharField(required=True, write_only=True, label='Подтверждение пароля')

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'patronymic', 'email', 'phone_number', 'password', 'password_confirmation']

    def validate(self, data):
        if data.get('password') != data.get('password_confirmation'):
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.patronymic = validated_data.get('patronymic', instance.patronymic)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)

        password = validated_data.get('password')
        if password:
            instance.set_password(password)

        instance.save()
        return instance
