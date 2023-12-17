from django.db import models
from rest_framework import serializers

from deceased_app.models import Deceased


class DeceasedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deceased
        fields = '__all__'


class DeceasedFromCemeteryPlotSerializer(DeceasedSerializer):
    id = serializers.ChoiceField(choices=[(obj.id, str(obj)) for obj in Deceased.objects.all()], label='Усопший')

    class Meta:
        model = Deceased
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(DeceasedFromCemeteryPlotSerializer, self).__init__(*args, **kwargs)
        self.fields['id'].choices = [(obj.id, str(obj)) for obj in Deceased.objects.all()]


class DeceasedListSerializer(DeceasedSerializer):
    is_favourite = serializers.SerializerMethodField()

    class Meta:
        model = Deceased
        exclude = ['favourites']

    def get_is_favourite(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.favourites.filter(id=request.user.id).exists()
        return False


class DeceasedCreateSerializer(DeceasedSerializer):
    class Meta:
        model = Deceased
        exclude = ['id', 'cemetery_plot']


class DeceasedFavouriteListSerializer(DeceasedSerializer):
    class Meta:
        model = Deceased
        exclude = ['cemetery_plot', 'favourites']


class DeceasedFavouriteSerializer(DeceasedSerializer):
    class Meta:
        model = Deceased
        fields = ['id']


class DeceasedForOrderSerializer(serializers.ModelSerializer):
    cemetery_name = serializers.CharField(source='cemetery_plot.cemetery.name')
    cemetery_municipality_name = serializers.CharField(source='cemetery_plot.cemetery.municipality.name')

    class Meta:
        model = Deceased
        fields = ['first_name', 'last_name', 'patronymic', 'cemetery_name', 'cemetery_municipality_name']
