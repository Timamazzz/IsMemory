from django_filters import rest_framework as filters
from rest_framework import serializers

from deceased_app.models import Deceased
from locations_app.models import Cemetery


class DeceasedFilter(filters.FilterSet):
    last_name = filters.CharFilter(lookup_expr='icontains', label='Фамилия')
    first_name = filters.CharFilter(lookup_expr='icontains', label='Имя')
    patronymic = filters.CharFilter(lookup_expr='icontains', label='Отчество')

    birth_date = filters.NumberFilter(field_name='birth_date', lookup_expr='year__lte', label='Год рождения до')
    death_date = filters.NumberFilter(field_name='death_date', lookup_expr='year__lte', label='Год смерти до')

    cemetery_plot = filters.CharFilter(field_name="cemetery_plot__cemetery__id", lookup_expr='exact',
                                       label='Кладбище')

    cemetery_plot_number = filters.CharFilter(field_name="cemetery_plot__plot_number", lookup_expr='icontains',
                                              label='Номер участка')

    class Meta:
        model = Deceased
        fields = ['last_name', 'first_name', 'patronymic', 'birth_date', 'death_date', 'cemetery_plot', 'cemetery_plot_number']


class DeceasedFilterSerializer(serializers.Serializer):
    last_name = serializers.CharField(required=False, label='Фамилия')
    first_name = serializers.CharField(required=False, label='Имя')
    patronymic = serializers.CharField(required=False, label='Отчество')

    birth_date = serializers.DateField(required=False, label='Год рождения до')
    death_date = serializers.DateField(required=False, label='Год смерти до')

    cemetery_plot = serializers.PrimaryKeyRelatedField(queryset=Cemetery.objects.all(), many=False, required=False,
                                                       label="Кладбище")

    cemetery_plot_number = serializers.CharField(required=False, label='Номер участка')

    class Meta:
        model = Deceased
        fields = ['last_name', 'first_name', 'patronymic', 'birth_date', 'death_date', 'cemetery_plot',
                  'cemetery_plot_number']
