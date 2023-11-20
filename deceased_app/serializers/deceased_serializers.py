from django.db import models
from rest_framework import serializers

from deceased_app.models import Deceased


class DeceasedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deceased
        fields = '__all__'


class DeceasedFromCemeteryPlotSerializer(DeceasedSerializer):
    id = serializers.ChoiceField(choices=[(obj.id, str(obj)) for obj in Deceased.objects.all()])
    deceased_choices = serializers.SerializerMethodField(read_only=False)

    class Meta:
        model = Deceased
        fields = '__all__'

    def get_deceased_choices(self, obj):
        choices = [
            {"value": deceased.id, "display_name": str(deceased)}
            for deceased in Deceased.objects.all()
        ]
        return {"type": "choice", "required": False, "read_only": False, "label": "Deceased choices yuas", "choices": choices}


class DeceasedCreateSerializer(DeceasedSerializer):
    class Meta:
        model = Deceased
        exclude = ['id', 'cemetery_plot']
