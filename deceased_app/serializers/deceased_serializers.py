from rest_framework import serializers

from deceased_app.models import Deceased


class DeceasedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deceased
        fields = '__all__'


class DeceasedFromCemeteryPlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deceased
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['id'] = {
            'value': instance.id,
            'display_text': f"Id {instance.id} - {instance.first_name} {instance.last_name} {instance.patronymic}"
        }
        return representation
