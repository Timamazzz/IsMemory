from django_filters import rest_framework as filters
from rest_framework import serializers

from IsMemory.helpers.filters import MultipleValueFilter
from locations_app.enums import CemeteryPlotStatusEnum, CemeteryPlotTypeEnum
from locations_app.models import Cemetery, Municipality, CemeteryPlot
from django.forms.fields import CharField


class CemeteryFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')
    municipality = filters.CharFilter(field_name="municipality__id", lookup_expr='exact')
    cemetery = filters.CharFilter(field_name="cemetery__id", lookup_expr='exact')

    class Meta:
        model = Cemetery
        fields = ['name', 'municipality', 'cemetery']


class CemeteryFilterSerializer(serializers.Serializer):
    name = serializers.CharField(required=False, label="Наименование кладбища")
    municipality = serializers.PrimaryKeyRelatedField(queryset=Municipality.objects.all(), many=False, required=False,
                                                      label="Муниципальное образование")
    cemetery = serializers.PrimaryKeyRelatedField(queryset=Cemetery.objects.all(), many=False, required=False,
                                                  label="Кладбище")

    class Meta:
        fields = ('name', 'municipality', 'cemetery')


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

    type = MultipleValueFilter(field_class=CharField)
    status = MultipleValueFilter(field_class=CharField)

    plot_number = filters.CharFilter(field_name='plot_number', lookup_expr='icontains')

    deceased_first_name = filters.CharFilter(field_name='cemetery_plot_set__first_name', lookup_expr='icontains')
    deceased_last_name = filters.CharFilter(field_name='cemetery_plot_set__last_name', lookup_expr='icontains')
    deceased_patronymic = filters.CharFilter(field_name='cemetery_plot_set__patronymic', lookup_expr='icontains')

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

    deceased_last_name = serializers.CharField(required=False, label="Фамилия усопшего")
    deceased_first_name = serializers.CharField(required=False, label="Имя усопшего")
    deceased_patronymic = serializers.CharField(required=False, label="Отчество усопшего")

    sector = serializers.CharField(required=False, label="Сектор")
    row = serializers.CharField(required=False, label="Ряд")
    burial = serializers.CharField(required=False, label="Захоронение")
    place = serializers.CharField(required=False, label="Место")

    class Meta:
        fields = ["cemetery", "municipality", "type", "status", 'plot_number', 'sector', 'row', 'burial', 'place', ]
