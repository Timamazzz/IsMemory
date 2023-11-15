from rest_framework import serializers

from locations_app.models import CemeteryPlot


class CemeteryPlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = CemeteryPlot
        fields = '__all__'


class CemeteryPlotListSerializer(serializers.ModelSerializer):
    municipality = serializers.CharField(source='micro_district.municipality.name', read_only=True,
                                         label="Муниципальное образование")
    type = serializers.CharField(source='get_type_display', read_only=True, label="Тип")
    status = serializers.CharField(source='get_status_display', read_only=True, label="Статус")
    cemetery = serializers.CharField(source='cemetery.name', read_only=True, label="Кладбище")

    class Meta:
        model = CemeteryPlot
        fields = ('id', 'cemetery', 'municipality', 'type', 'plot_number', 'sector', 'row', 'burial',
                  'place', 'status')
