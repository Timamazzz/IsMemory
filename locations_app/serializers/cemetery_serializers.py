import ast

from django.db.models import Q
from rest_framework import serializers

from locations_app.enums import CemeteryPlotStatusEnum, CemeteryPlotTypeEnum
from locations_app.models import Cemetery, Municipality, CemeteryPlot
from locations_app.serializers.cemetery_plot_serializers import CemeteryPlotMapSerializer
from shapely.geometry import Polygon, Point


class CemeterySerializer(serializers.ModelSerializer):
    class Meta:
        model = Cemetery
        fields = '__all__'


class CemeteryListSerializer(CemeterySerializer):
    municipality = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='name',
        label='Муниципальное образование'
    )

    cemetery_plots_count = serializers.ReadOnlyField(label='Общее количество участков на кладбище')
    cemetery_plots_free = serializers.ReadOnlyField(label='Количество свободных участков на кладбище')
    cemetery_plots_occupied = serializers.ReadOnlyField(label='Количество занятых участков на кладбище')
    cemetery_plots_inventory = serializers.ReadOnlyField(label='Количество участков в инвентаризации на кладбище')

    class Meta:
        model = Cemetery
        fields = ('id', 'name', 'municipality', 'cemetery_plots_count', 'cemetery_plots_free',
                  'cemetery_plots_occupied', 'cemetery_plots_inventory')


class CemeteryTotalSerializer(CemeterySerializer):
    cemetery_plots_count = serializers.ReadOnlyField()
    cemetery_plots_free = serializers.ReadOnlyField()
    cemetery_plots_occupied = serializers.ReadOnlyField()
    cemetery_plots_inventory = serializers.ReadOnlyField()


class CemeteryRetrieveSerializer(CemeterySerializer):
    class Meta:
        model = Cemetery
        fields = '__all__'


class CemeteryCreateSerializer(CemeterySerializer):
    municipality = serializers.PrimaryKeyRelatedField(queryset=Municipality.objects.all(), many=False, required=True,
                                                      allow_null=False,
                                                      label="Муниципальное образование")

    class Meta:
        model = Cemetery
        fields = '__all__'
        depth = 1


class CemeteryUpdateSerializer(CemeterySerializer):
    municipality = serializers.PrimaryKeyRelatedField(queryset=Municipality.objects.all(), many=False, required=True,
                                                      allow_null=False,
                                                      label="Муниципальное образование")

    class Meta:
        model = Cemetery
        fields = '__all__'
        depth = 1


class CemeteryMapSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Cemetery.objects.all())
    cemetery_plots = serializers.SerializerMethodField()

    for_free_plots_count = serializers.SerializerMethodField()
    for_occupied_plots_count = serializers.SerializerMethodField()
    for_inventory_plots_count = serializers.SerializerMethodField()

    burial_plots_count = serializers.SerializerMethodField()
    vacant_plots_count = serializers.SerializerMethodField()

    class Meta:
        model = Cemetery
        fields = ['id', 'name', 'coordinates', 'cemetery_plots', 'for_free_plots_count', 'for_occupied_plots_count',
                  'for_inventory_plots_count', 'burial_plots_count', 'vacant_plots_count']

    def get_cemetery_plots(self, obj):
        request = self.context.get('request')
        if request:
            statuses = request.query_params.get('status', None)
            types = request.query_params.get('type', None)
            visible_area_coords = request.query_params.get('visible_area_coords', None)

            ignore_filters = 'ignore_filters' in request.query_params

            cemetery_plots = CemeteryPlot.objects.filter(cemetery=obj)

            if not ignore_filters:
                statuses = statuses.split(',') if statuses else None
                types = types.split(',') if types else None

                status_filters = Q(status=None)
                type_filters = Q(type=None)

                if statuses:
                    status_filters = Q()
                    for status in statuses:
                        status_filters |= Q(status=status)

                if types:
                    type_filters = Q()
                    for type in types:
                        type_filters |= Q(type=type)

                cemetery_plots = cemetery_plots.filter(status_filters, type_filters)

                if visible_area_coords:
                    print("Visible area coordinates before evaluation:", visible_area_coords)
                    visible_area_coords = ast.literal_eval(visible_area_coords)
                    print("Visible area coordinates after evaluation:", visible_area_coords)
                    visible_area_polygon = Polygon(visible_area_coords)
                    print("Visible area polygon:", visible_area_polygon)
                    plots_in_visible_area = []
                    for plot in cemetery_plots:
                        if plot.coordinates:
                            plot_polygon = Polygon(plot.coordinates[0])
                            print("Plot polygon:", plot_polygon)
                            if plot_polygon.intersects(visible_area_polygon):
                                plots_in_visible_area.append(plot)
                    print("Plots in visible area:", plots_in_visible_area)
                    return CemeteryPlotMapSerializer(plots_in_visible_area, many=True).data

            return CemeteryPlotMapSerializer(cemetery_plots, many=True).data

    @staticmethod
    def get_for_free_plots_count(obj):
        return CemeteryPlot.objects.filter(cemetery=obj, status=CemeteryPlotStatusEnum.FREE.name).count()

    @staticmethod
    def get_for_occupied_plots_count(obj):
        return CemeteryPlot.objects.filter(cemetery=obj, status=CemeteryPlotStatusEnum.OCCUPIED.name).count()

    @staticmethod
    def get_for_inventory_plots_count(obj):
        return CemeteryPlot.objects.filter(cemetery=obj, status=CemeteryPlotStatusEnum.INVENTORY.name).count()

    @staticmethod
    def get_burial_plots_count(obj):
        return CemeteryPlot.objects.filter(cemetery=obj, type=CemeteryPlotTypeEnum.BURIAL.name).count()

    @staticmethod
    def get_vacant_plots_count(obj):
        return CemeteryPlot.objects.filter(cemetery=obj, type=CemeteryPlotTypeEnum.VACANT.name).count()
