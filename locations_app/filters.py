from django_filters import rest_framework as filters
from rest_framework import serializers

from locations_app.enums import CemeteryPlotStatusEnum, CemeteryPlotTypeEnum
from locations_app.models import Cemetery, Municipality


class CemeteryFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')
    municipality = filters.CharFilter(field_name="municipality__id", lookup_expr='exact')

    class Meta:
        model = Cemetery
        fields = ['name', 'municipality']


class CemeteryMapFilterSerializer(serializers.Serializer):
    status = serializers.ChoiceField(
        choices=[(enum.name, enum.value) for enum in CemeteryPlotStatusEnum],
        required=False,
        label="Статус"
    )
    type = serializers.ChoiceField(
        choices=[(enum.name, enum.value) for enum in CemeteryPlotTypeEnum],
        required=False,
        label="Категория"
    )

    class Meta:
        fields = ("status", "type",)


class CemeteryFilterSerializer(serializers.Serializer):
    name = serializers.CharField(required=False, label="Наименование кладбища")
    municipality = serializers.PrimaryKeyRelatedField(queryset=Municipality.objects.all(), many=False, required=False,
                                                      label="Муниципальное образование")

    class Meta:
        fields = ('name', 'municipality')
