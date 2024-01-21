import os
import uuid

from django.contrib.auth.models import AnonymousUser
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from IsMemory.helpers.CustomModelViewSet import CustomModelViewSet
from IsMemory.helpers.UploadMultipleFileImageMixin import UploadMultipleFileImageMixin
from orders_app.enums import OrderStatusEnum
from orders_app.models import Order, Executor
from orders_app.serializers.executor_serializers import (ExecutorSerializer, ExecutorCreateSerializer,
                                                         ExecutorSetDataSerializer)
from orders_app.serializers.order_serializers import OrderSerializer, OrderCreateSerializer, OrderListSerializer, \
    OrderUpdateSerializer, OrderDetailSerializer

from yookassa import Configuration, Payment

from services_app.models import Service


# Create your views here.
class OrderViewSet(CustomModelViewSet, UploadMultipleFileImageMixin):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    serializer_list = {
        'list': OrderListSerializer,
        'create': OrderCreateSerializer,
        'update': OrderUpdateSerializer,
        'retrieve': OrderDetailSerializer,
    }

    def get_queryset(self):
        if isinstance(self.request.user, AnonymousUser):
            return Order.objects.all()
        else:
            return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['GET'])
    def get_orders_by_chat_id(self, request, *args, **kwargs):
        chat_id = request.query_params.get('chat_id')

        if not chat_id:
            return Response({"error": "Chat id is required"}, status=status.HTTP_400_BAD_REQUEST)

        orders = Order.objects.filter(executor__chat_id=chat_id, status=OrderStatusEnum.WORK_IN_PROGRESS.name)

        if not orders.exists():
            return Response({"message": "No orders found for the specified Chat id"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = OrderListSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        serializer = OrderUpdateSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data.update({'user': request.user.id})

        Configuration.account_id = '307382'
        Configuration.secret_key = 'test_3uCnUvpBAqwu2MFOFsyc-9ORVYRZPzcA_rMGX0AHB4Q'

        service = Service.objects.get(id=data['service'])
        payment = Payment.create({
            "amount": {
                "value": f"{data['count'] * service.price}",
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "https://belmemorial.ru/account"
            },
            "capture": True,
            "description": f""
        }, uuid.uuid4())

        data.update({'payment_id': payment.id})
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response = serializer.data.copy()
        response.update({'url': payment.confirmation.confirmation_url})
        return Response(response, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['POST'])
    def payments(self, request, *args, **kwargs):
        data = request.data
        project_folder = os.path.dirname(os.path.abspath(__file__))
        file_name = 'received_data.txt'
        file_path = os.path.join(project_folder, file_name)
        with open(file_path, 'w') as file:
            file.write(str(data))
        return Response({'status': 'Data received and saved successfully'}, status=status.HTTP_200_OK)


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
        if phone_number and phone_number.startswith('7'):
            phone_number = '+' + phone_number
        chat_id = request.data.get('chat_id')
        try:
            executor = Executor.objects.get(phone_number=phone_number)
            executor.chat_id = chat_id
            executor.save()
            serializer = ExecutorSerializer(executor)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Executor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
