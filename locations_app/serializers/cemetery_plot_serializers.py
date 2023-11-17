from rest_framework import serializers

from deceased_app.serializers.deceased_serializers import DeceasedFromCemeteryPlotSerializer
from locations_app.models import CemeteryPlot


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


class CemeteryPlotTabsSerializer(serializers.Serializer):
    cemetery_plot = CemeteryPlotSerializer(many=False)
    deceased = DeceasedFromCemeteryPlotSerializer(many=True)

