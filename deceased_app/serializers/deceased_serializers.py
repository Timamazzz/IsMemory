from django.db import models
from rest_framework import serializers

from deceased_app.models import Deceased


class DeceasedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deceased
        fields = '__all__'


class DeceasedFromCemeteryPlotSerializer(DeceasedSerializer):
    id = serializers.ChoiceField(choices=[(obj.id, str(obj)) for obj in Deceased.objects.all()])

    class Meta:
        model = Deceased
        fields = '__all__'


class DeceasedCreateSerializer(DeceasedSerializer):

    class Meta:
        model = Deceased
        exclude = ['id', 'cemetery_plot']
