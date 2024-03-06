from rest_framework import serializers

from deceased_app.serializers.deceased_serializers import DeceasedFromCemeteryPlotSerializer
from docs_app.models import CemeteryPlotImage
from locations_app.models import CemeteryPlot
from drf_writable_nested.serializers import WritableNestedModelSerializer


class CemeteryPlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = CemeteryPlot
        fields = '__all__'


class CemeteryPlotListSerializer(CemeteryPlotSerializer):
    municipality = serializers.CharField(source='cemetery.municipality.name', read_only=True,
                                         label="Муниципальное образование")
    type = serializers.CharField(source='get_type_display', read_only=True, label="Тип")
    status = serializers.CharField(source='get_status_display', read_only=True, label="Статус")
    cemetery = serializers.CharField(source='cemetery.name', read_only=True, label="Кладбище")

    class Meta:
        model = CemeteryPlot
        fields = ('id', 'cemetery', 'municipality', 'type', 'plot_number', 'sector', 'row', 'burial',
                  'place', 'status')


class CemeteryPlotCreateSerializer(CemeteryPlotSerializer):
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


class CemeteryPlotRetrieveSerializer(CemeteryPlotSerializer):
    deceased = DeceasedFromCemeteryPlotSerializer(many=True, source='cemetery_plot_set')
    images = CemeteryPlotImageSerializer(many=True, read_only=True)

    class Meta:
        model = CemeteryPlot
        fields = '__all__'


class CemeteryPlotUpdateSerializer(WritableNestedModelSerializer):
    deceased = DeceasedFromCemeteryPlotSerializer(many=True, source='cemetery_plot_set')

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
    preview_image = serializers.SerializerMethodField()

    def get_preview_image(self, obj):
        preview_image = obj.images.filter(is_preview=True).first()
        if preview_image:
            return preview_image.file.url
        return None

    class Meta:
        model = CemeteryPlot
        fields = ('id', 'type', 'plot_number', 'sector', 'row', 'burial', 'place', 'status', 'coordinates')
