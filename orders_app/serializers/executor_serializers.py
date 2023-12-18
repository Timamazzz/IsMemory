from rest_framework import serializers
from orders_app.models import Executor


class ExecutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Executor
        fields = '__all__'


class ExecutorCreateSerializer(ExecutorSerializer):
    class Meta:
        model = Executor
        fields = []


class ExecutorSetDataSerializer(ExecutorSerializer):
    class Meta:
        model = Executor
        fields = ['chat_id', 'phone_number']
