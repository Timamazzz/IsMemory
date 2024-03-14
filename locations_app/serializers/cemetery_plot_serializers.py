from rest_framework import serializers

from deceased_app.serializers.deceased_serializers import DeceasedFromCemeteryPlotSerializer
from docs_app.models import CemeteryPlotImage
from docs_app.serializers.cemetery_plot_serializers import CemeteryPlotImageFromPlotSerializer, \
    CemeteryPlotCreateUpdateImageFromPlotSerializer
from locations_app.models import CemeteryPlot
from drf_writable_nested.serializers import WritableNestedModelSerializer


class CemeteryPlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = CemeteryPlot
        fields = '__all__'


class CemeteryPlotListSerializer(CemeteryPlotSerializer):
    municipality = serializers.CharField(source='cemetery.municipality.name', read_only=True, label="Муниципальное образование")
    type = serializers.CharField(source='get_type_display', read_only=True, label="Тип")
    status = serializers.CharField(source='get_status_display', read_only=True, label="Статус")
    cemetery = serializers.CharField(source='cemetery.name', read_only=True, label="Кладбище")
    first_name = serializers.CharField(source='cemetery_plot_set.first_name', read_only=True, label="Имя")
    last_name = serializers.CharField(source='cemetery_plot_set.last_name', read_only=True, label="Фамилия")
    patronymic = serializers.CharField(source='cemetery_plot_set.patronymic', read_only=True, label="Отчество")

    class Meta:
        model = CemeteryPlot
        fields = ('id', 'cemetery', 'municipality', 'type', 'plot_number', 'sector', 'row', 'burial', 'place', 'status', 'first_name', 'last_name', 'patronymic')



class CemeteryPlotCreateSerializer(WritableNestedModelSerializer):
    images = CemeteryPlotCreateUpdateImageFromPlotSerializer(many=True, required=False)

    class Meta:
        model = CemeteryPlot
        fields = '__all__'


class CemeteryPlotImageSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = CemeteryPlotImage
        fields = ['url', 'is_preview']

    def get_url(self, obj):
        return obj.file.url


class CemeteryPlotRetrieveSerializer(WritableNestedModelSerializer):
    deceased = DeceasedFromCemeteryPlotSerializer(many=True, source='cemetery_plot_set')
    images = CemeteryPlotImageFromPlotSerializer(many=True, read_only=True)

    class Meta:
        model = CemeteryPlot
        fields = ['id', 'cemetery', 'coordinates', 'plot_number', 'sector', 'row', 'burial', 'place', 'type', 'status', 'description', 'note', 'images', 'deceased']


class CemeteryPlotUpdateSerializer(WritableNestedModelSerializer):
    deceased = DeceasedFromCemeteryPlotSerializer(many=True, source='cemetery_plot_set')
    images = CemeteryPlotCreateUpdateImageFromPlotSerializer(many=True, required=False)

    class Meta:
        model = CemeteryPlot
        fields = '__all__'


class CemeteryPlotMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = CemeteryPlot
        fields = ['id', 'plot_number', 'coordinates', 'status', 'type']


class CemeteryPlotListMapSerializer(CemeteryPlotSerializer):
    type = serializers.CharField(source='get_type_display', read_only=True, label="Тип")
    status = serializers.CharField(source='get_status_display', read_only=True, label="Статус")

    class Meta:
        model = CemeteryPlot
        fields = ('id', 'type', 'plot_number', 'sector', 'row', 'burial', 'place', 'status', 'coordinates')
