from django_filters import rest_framework as filters
from rest_framework import serializers

from locations_app.enums import CemeteryPlotStatusEnum, CemeteryPlotTypeEnum
from locations_app.models import Cemetery, Municipality, CemeteryPlot


class CemeteryFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')
    municipality = filters.CharFilter(field_name="municipality__id", lookup_expr='exact')

    class Meta:
        model = Cemetery
        fields = ['name', 'municipality']


class CemeteryFilterSerializer(serializers.Serializer):
    name = serializers.CharField(required=False, label="Наименование кладбища")
    municipality = serializers.PrimaryKeyRelatedField(queryset=Municipality.objects.all(), many=False, required=False,
                                                      label="Муниципальное образование")

    class Meta:
        fields = ('name', 'municipality')


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


class CemeteryPlotFilter(filters.FilterSet):
    cemetery = filters.CharFilter(field_name="cemetery__id", lookup_expr='exact')
    municipality = filters.CharFilter(field_name="cemetery__municipality__id", lookup_expr='exact')

    type = filters.ChoiceFilter(choices=[(enum.name, enum.value) for enum in CemeteryPlotTypeEnum], field_name='type')
    status = filters.ChoiceFilter(choices=[(enum.name, enum.value) for enum in CemeteryPlotStatusEnum],
                                  field_name='status')

    plot_number = filters.CharFilter(field_name='plot_number', lookup_expr='icontains')
    sector = filters.CharFilter(field_name='sector', lookup_expr='icontains')
    row = filters.CharFilter(field_name='row', lookup_expr='icontains')
    burial = filters.CharFilter(field_name='burial', lookup_expr='icontains')
    place = filters.CharFilter(field_name='place', lookup_expr='icontains')

    class Meta:
        model = CemeteryPlot
        fields = ['cemetery', 'municipality', 'type', 'status', 'plot_number', 'sector', 'row', 'burial', 'place']


class CemeteryPlotFilterSerializers(serializers.Serializer):
    cemetery = serializers.PrimaryKeyRelatedField(queryset=Cemetery.objects.all(), many=False,
                                                  required=False, label="Кладбище")
    municipality = serializers.PrimaryKeyRelatedField(queryset=Municipality.objects.all(), many=False, required=False,
                                                      label="Муниципальное образование")
    type = serializers.ChoiceField(choices=[(type.name, type.value) for type in CemeteryPlotTypeEnum], required=False,
                                   label="Тип")
    status = serializers.ChoiceField(choices=[(status.name, status.value) for status in CemeteryPlotStatusEnum],
                                     required=False, label="Статус")

    plot_number = serializers.CharField(required=False, label="Номер участка")
    sector = serializers.CharField(required=False, label="Сектор")
    row = serializers.CharField(required=False, label="Ряд")
    burial = serializers.CharField(required=False, label="Захоронение")
    place = serializers.CharField(required=False, label="Место")

    class Meta:
        fields = ["cemetery", "municipality", "type", "status", 'plot_number', 'sector', 'row', 'burial', 'place',]
