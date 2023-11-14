from rest_framework import serializers

from locations_app.models import Cemetery, Municipality


class CemeterySerializer(serializers.ModelSerializer):
    class Meta:
        model = Cemetery
        fields = '__all__'


class CemeteryListSerializer(serializers.ModelSerializer):
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


class CemeteryTotalSerializer(serializers.Serializer):
    cemetery_plots_count = serializers.ReadOnlyField()
    cemetery_plots_free = serializers.ReadOnlyField()
    cemetery_plots_occupied = serializers.ReadOnlyField()
    cemetery_plots_inventory = serializers.ReadOnlyField()


class CemeteryRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cemetery
        fields = '__all__'


class CemeteryCreateSerializer(serializers.ModelSerializer):
    municipality = serializers.PrimaryKeyRelatedField(queryset=Municipality.objects.all(), many=False, required=True,
                                                      allow_null=False,
                                                      label="Муниципальное образование")

    class Meta:
        model = Cemetery
        fields = '__all__'
        depth = 1