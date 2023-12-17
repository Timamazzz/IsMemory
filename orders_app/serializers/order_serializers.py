from rest_framework import serializers

from deceased_app.serializers.deceased_serializers import DeceasedForOrderSerializer
from orders_app.models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderListSerializer(OrderSerializer):
    service_name = serializers.CharField(source='service.name')
    deceased = DeceasedForOrderSerializer()

    class Meta:
        model = Order
        fields = ['id', 'date', 'status', 'service_name', 'deceased', 'comment', 'is_good', 'is_bad']


class OrderCreateSerializer(OrderSerializer):
    class Meta:
        model = Order
        fields = ['service', 'deceased']
