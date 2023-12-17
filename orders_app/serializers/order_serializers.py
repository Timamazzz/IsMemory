from rest_framework import serializers

from orders_app.models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderListSerializer(OrderSerializer):
    class Meta:
        model = Order
        fields = ['id', 'date', 'status', 'service', 'deceased', 'comment', 'is_good', 'is_bad']


class OrderCreateSerializer(OrderSerializer):
    class Meta:
        model = Order
        fields = ['service', 'deceased']
