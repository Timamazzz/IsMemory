from django_filters import rest_framework as filters
from locations_app.models import Cemetery


class CemeteryFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    municipality = filters.CharFilter(field_name="municipality__id", lookup_expr='exact')

    class Meta:
        model = Cemetery
        fields = ['name', 'municipality']