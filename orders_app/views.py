from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

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

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['GET'])
    def get_orders_by_phone(self, request, *args, **kwargs):
        phone_number = request.query_params.get('phone_number')

        if not phone_number:
            return Response({"error": "Phone number is required"}, status=status.HTTP_400_BAD_REQUEST)

        orders = Order.objects.filter(executor__phone_number=phone_number)

        if not orders.exists():
            return Response({"message": "No orders found for the specified phone number"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = OrderListSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
