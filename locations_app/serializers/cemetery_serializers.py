from django.db.models import Q
from rest_framework import serializers

from locations_app.enums import CemeteryPlotStatusEnum, CemeteryPlotTypeEnum
from locations_app.models import Cemetery, Municipality, CemeteryPlot


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

    cemetery_plots_count = serializers.ReadOnlyField()
    cemetery_plots_free = serializers.ReadOnlyField()
    cemetery_plots_occupied = serializers.ReadOnlyField()
    cemetery_plots_inventory = serializers.ReadOnlyField()

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


class CemeteryMapSerializer(CemeterySerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Cemetery.objects.all())
    cemetery_plots = serializers.SerializerMethodField()

    class Meta:
        model = Cemetery
        fields = ['id', 'name', 'coordinates', 'cemetery_plots']

    def get_cemetery_plots(self, obj):
        request = self.context.get('request')
        statuses = request.query_params.get('status', None)
        types = request.query_params.get('type', None)

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

        return CemeteryMapSerializer(cemetery_plots, many=True).data


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
