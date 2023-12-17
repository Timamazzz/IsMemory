from rest_framework import permissions

from IsMemory.helpers.CustomModelViewSet import CustomModelViewSet
from orders_app.models import Order
from orders_app.serializers.order_serializers import OrderSerializer, OrderCreateSerializer, OrderListSerializer


# Create your views here.
class OrderViewSet(CustomModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    serializer_list = {
        'list': OrderListSerializer,
        'create': OrderCreateSerializer,
    }

    permission_classes = [permissions.IsAuthenticated]
