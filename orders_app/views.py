import decimal
import json
import os
import uuid

from django.contrib.auth.models import AnonymousUser
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from yookassa.domain.notification import WebhookNotificationFactory, WebhookNotificationEventType

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

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        order_serializer = self.get_serializer(data=serializer.data)
        order_serializer.is_valid(raise_exception=True)
        order_instance = self.perform_create(order_serializer)

        Configuration.configure('307382', 'test_3uCnUvpBAqwu2MFOFsyc-9ORVYRZPzcA_rMGX0AHB4Q')

        service = Service.objects.get(id=data['service'])
        idempotence_key = order_instance.id
        payment = Payment.create({
            "amount": {
                "value": f"{decimal.Decimal(data['count']) * service.price}",
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "https://belmemorial.ru/account"
            },
            "capture": True,
            "description": f"Заказ № {order_instance.id}",
            "idempotence_key": idempotence_key,
        }, idempotence_key)

        order_instance.payment_id = payment.id
        order_instance.save()

        headers = self.get_success_headers(serializer.data)
        response = {
            'order': data,
            'redirect': {
                'url': payment.confirmation.confirmation_url
            }
        }

        return Response(response, status=status.HTTP_201_CREATED, headers=headers)

    # @action(detail=False, methods=['POST'])
    # def payments(self, request, *args, **kwargs):
    #     data = request.data.object.copy()
    #
    #     file_path = '/sites/IsMemory/IsMemory/data.txt'
    #     with open(file_path, 'w') as file:
    #         file.write(str(data))
    #
    #     order = get_object_or_404(Order, payment_id=data.id)
    #
    #     if data.status == 'succeeded':
    #         order.status = OrderStatusEnum.WORK_IN_PROGRESS.name
    #         order.save()
    #     elif data.status == 'canceled':
    #         order.status = OrderStatusEnum.CANCELLED.name
    #         order.save()
    #
    #     file_path = '/sites/IsMemory/IsMemory/order.txt'
    #     with open(file_path, 'w') as file:
    #         file.write(str(order))
    #
    #     return Response({
    #         'detail': 'Order status updated successfully',
    #         'order_id': order.id,
    #         'new_status': order.status,
    #     }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def payments(self, request, *args, **kwargs):
        event_json = json.loads(request.data)
        file_path = '/sites/IsMemory/IsMemory/event_json.txt'
        with open(file_path, 'w') as file:
            file.write(str(event_json))
        try:
            notification_object = WebhookNotificationFactory().create(event_json)
            response_object = notification_object.object
            file_path = '/sites/IsMemory/IsMemory/response_object.txt'
            with open(file_path, 'w') as file:
                file.write(str(response_object))
            if notification_object.event == WebhookNotificationEventType.PAYMENT_SUCCEEDED or notification_object.event == WebhookNotificationEventType.PAYMENT_CANCELED:
                some_data = {
                    'paymentId': response_object.id,
                    'paymentStatus': response_object.status,
                }
            else:
                return Response({}, status=400)

            Configuration.configure('307382', 'test_3uCnUvpBAqwu2MFOFsyc-9ORVYRZPzcA_rMGX0AHB4Q')
            payment_info = Payment.find_one(some_data['paymentId'])
            file_path = '/sites/IsMemory/IsMemory/payment_info.txt'
            with open(file_path, 'w') as file:
                file.write(str(payment_info))
            if payment_info:
                order = Order.objects.get(payment_id=some_data['paymentId'])
                if payment_info.status == 'succeeded':
                    order.status = OrderStatusEnum.IN_QUEUE.name
                elif payment_info.status == 'canceled':
                    order.status = OrderStatusEnum.CANCELLED.name
                file_path = '/sites/IsMemory/IsMemory/data.txt'
                with open(file_path, 'w') as file:
                    file.write(str(order))
                order.save()
            else:
                return Response({}, status=400)

        except Exception:
            return Response({}, status=400)

        return Response({}, status=200)


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
