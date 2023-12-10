from rest_framework import serializers
from services_app.models import Service


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class ServiceListSerializer(ServiceSerializer):
    class Meta:
        model = Service
        fields = '__all__'
