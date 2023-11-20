from rest_framework import serializers

from deceased_app.serializers.deceased_serializers import DeceasedFromCemeteryPlotSerializer
from locations_app.models import CemeteryPlot
from drf_writable_nested.serializers import WritableNestedModelSerializer


class CemeteryPlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = CemeteryPlot
        fields = '__all__'


class CemeteryPlotListSerializer(CemeteryPlotSerializer):
    municipality = serializers.CharField(source='micro_district.municipality.name', read_only=True,
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


class CemeteryPlotRetrieveSerializer(CemeteryPlotSerializer):
    deceased = DeceasedFromCemeteryPlotSerializer(many=True, source='cemetery_plot_set')

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
        fields = ['id', 'name', 'coordinates', 'status', 'type']
