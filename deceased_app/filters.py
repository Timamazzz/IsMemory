from django_filters import rest_framework as filters
from rest_framework import serializers

from deceased_app.models import Deceased
from locations_app.models import Cemetery


class DeceasedFilter(filters.FilterSet):
    first_name = filters.CharFilter(lookup_expr='icontains', label='Имя')
    last_name = filters.CharFilter(lookup_expr='icontains', label='Фамилия')
    patronymic = filters.CharFilter(lookup_expr='icontains', label='Отчество')

    birth_date__lte = filters.NumberFilter(field_name='birth_date', lookup_expr='year__lte',
                                           label='Год рождения до')
    death_date__lte = filters.NumberFilter(field_name='death_date', lookup_expr='year__lte',
                                           label='Год смерти до')

    cemetery_plot = filters.CharFilter(field_name="cemetery_plot__cemetery__id", lookup_expr='exact',
                                       label='Кладбище')

    class Meta:
        model = Deceased
        fields = ['first_name', 'last_name', 'patronymic', 'birth_date__lte', 'death_date__lte', 'cemetery_plot']


class DeceasedFilterSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False, label='Имя')
    last_name = serializers.CharField(required=False, label='Фамилия')
    patronymic = serializers.CharField(required=False, label='Отчество')

    birth_date__lte = serializers.DateField(required=False, label='Год рождения до')
    death_date__lte = serializers.DateField(required=False, label='Год смерти до')

    cemetery_plot = serializers.PrimaryKeyRelatedField(queryset=Cemetery.objects.all(), many=False, required=False,
                                                       label="Кладбище")

    class Meta:
        model = Deceased
        fields = ['first_name', 'last_name', 'patronymic', 'birth_date__lte', 'death_date__lte', 'cemetery_plot']
