from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from deceased_app.serializers.deceased_serializers import DeceasedForOrderSerializer
from docs_app.models import OrderImage
from orders_app.models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderImageSerializer(serializers.ModelSerializer):
    file = serializers.ImageField(allow_empty_file=False)

    class Meta:
        model = OrderImage
        fields = '__all__'


class OrderDetailSerializer(OrderSerializer):
    images = OrderImageSerializer(source="images_order_rel", many=True, required=False)
    service_name = serializers.CharField(source="service.name", required=False)
    deceased = DeceasedForOrderSerializer()
    coordinates = serializers.SerializerMethodField()

    def get_coordinates(self, obj):
        if obj.deceased:
            if obj.deceased.cemetery_plot:
                return obj.deceased.cemetery_plot.coordinates
        return None

    class Meta:
        model = Order
        fields = '__all__'


class OrderListSerializer(OrderSerializer):
    service_name = serializers.CharField(source='service.name')
    deceased = DeceasedForOrderSerializer()
    images = OrderImageSerializer(source="images_order_rel", many=True, required=False)

    class Meta:
        model = Order
        fields = ['id', 'date', 'status', 'service_name', 'deceased', 'comment', 'is_good', 'is_bad', 'images']


class OrderCreateSerializer(OrderSerializer):
    class Meta:
        model = Order
        fields = ['service', 'deceased', 'count', 'user', 'payment_id']
        extra_kwargs = {
            'service': {'required': True},
            'deceased': {'required': True},
            'count': {'required': True},
        }


class OrderImageSerializerWriter(WritableNestedModelSerializer):
    file = serializers.CharField(allow_null=False, allow_blank=False)
    original_name = serializers.CharField(allow_blank=False, allow_null=False)

    class Meta:
        model = OrderImage
        fields = ['file', 'original_name']


class OrderUpdateSerializer(WritableNestedModelSerializer):
    images = OrderImageSerializerWriter(source="images_order_rel", many=True, required=False)

    class Meta:
        model = Order
        fields = ['id', 'comment', 'is_good', 'is_bad', 'status', 'images']
        read_only_fields = ['id']
