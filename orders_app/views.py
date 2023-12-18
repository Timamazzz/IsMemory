from django.contrib.auth.models import AnonymousUser
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from IsMemory.helpers.CustomModelViewSet import CustomModelViewSet
from orders_app.enums import OrderStatusEnum
from orders_app.models import Order, Executor
from orders_app.serializers.executor_serializers import (ExecutorSerializer, ExecutorCreateSerializer,
                                                         ExecutorSetDataSerializer)
from orders_app.serializers.order_serializers import OrderSerializer, OrderCreateSerializer, OrderListSerializer, \
    OrderUpdateSerializer


# Create your views here.
class OrderViewSet(CustomModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    serializer_list = {
        'list': OrderListSerializer,
        'create': OrderCreateSerializer,
        'update': OrderUpdateSerializer,
    }

    def get_queryset(self):
        if isinstance(self.request.user, AnonymousUser):
            return Order.objects.all()
        else:
            return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['GET'])
    def get_orders_by_phone(self, request, *args, **kwargs):
        phone_number = request.query_params.get('phone_number')

        if not phone_number:
            return Response({"error": "Phone number is required"}, status=status.HTTP_400_BAD_REQUEST)

        orders = Order.objects.filter(executor__phone_number=phone_number, status=OrderStatusEnum.WORK_IN_PROGRESS.name)

        if not orders.exists():
            return Response({"message": "No orders found for the specified phone number"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = OrderListSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ExecutorViewSet(CustomModelViewSet):
    queryset = Executor.objects.all()
    serializer_class = ExecutorSerializer
    serializer_list = {
        'create': ExecutorCreateSerializer,
        'set_data': ExecutorSetDataSerializer,
    }

    @action(detail=False, methods=['PUT'])
    def set_data(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        chat_id = request.data.get('chat_id')
        try:
            executor = Executor.objects.get(phone_number=phone_number)
            executor.chat_id = chat_id
            executor.save()
            serializer = ExecutorSerializer(executor)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Executor.DoesNotExist:
            executor = Executor.objects.create(chat_id=chat_id, phone_number=phone_number)
            serializer = ExecutorSerializer(executor)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

