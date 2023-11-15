from rest_framework import status, permissions
from rest_framework.response import Response

from IsMemory.helpers.CustomModelViewSet import CustomModelViewSet
from locations_app.enums import CemeteryPlotStatusEnum
from locations_app.models import Cemetery, CemeteryPlot
from locations_app.serializers.cemetery_plot_serializers import CemeteryPlotSerializer, CemeteryPlotListSerializer
from locations_app.serializers.cemetery_serializers import CemeterySerializer, CemeteryListSerializer, \
    CemeteryCreateSerializer, CemeteryRetrieveSerializer, CemeteryUpdateSerializer
from django.db.models import Count, Case, When, IntegerField


# Create your views here.
class CemeteryViewSet(CustomModelViewSet):
    queryset = Cemetery.objects.all()
    serializer_class = CemeterySerializer
    serializer_list = {
        'list': CemeteryListSerializer,
        'create': CemeteryCreateSerializer,
        'update': CemeteryUpdateSerializer,
        'retrieve': CemeteryRetrieveSerializer,
    }

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Cemetery.objects.annotate(
            cemetery_plots_count=Count('plots'),
            cemetery_plots_free=Count(Case(When(plots__status=CemeteryPlotStatusEnum.FREE.name, then=1),
                                           output_field=IntegerField())),
            cemetery_plots_occupied=Count(Case(When(plots__status=CemeteryPlotStatusEnum.OCCUPIED.name, then=1),
                                               output_field=IntegerField())),
            cemetery_plots_inventory=Count(Case(When(plots__status=CemeteryPlotStatusEnum.INVENTORY.name, then=1),
                                                output_field=IntegerField())),
        )
        return queryset

    def list(self, request, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = CemeteryListSerializer(queryset, many=True)
        response_data = {'count': queryset.count(), 'cemeteries': serializer.data}

        return Response(response_data, status=status.HTTP_200_OK)


class CemeteryPlotViewSet(CustomModelViewSet):
    queryset = CemeteryPlot.objects.all()
    serializer_class = CemeteryPlotSerializer
    serializer_list = {
        'list': CemeteryPlotListSerializer,
    }

    #permission_classes = [permissions.IsAuthenticated]
