from rest_framework import serializers

from docs_app.models import CemeteryPlotImage


class CemeteryPlotImageFromPlotSerializer(serializers.ModelSerializer):


    class Meta:
        model = CemeteryPlotImage
        fields = ('id', 'file', 'original_name', 'is_preview')


class CemeteryPlotCreateUpdateImageFromPlotSerializer(serializers.ModelSerializer):

    class Meta:
        model = CemeteryPlotImage
        fields = ('id', 'file', 'original_name', 'is_preview')
