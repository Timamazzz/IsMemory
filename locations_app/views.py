from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action

from users_app.admin_permissions import HasDashboardAdminGroupPermission
from IsMemory.helpers.CustomModelViewSet import CustomModelViewSet
from locations_app.enums import CemeteryPlotStatusEnum
from locations_app.filters import CemeteryFilter, CemeteryMapFilterSerializer, CemeteryFilterSerializer, \
    CemeteryPlotFilter, CemeteryPlotFilterSerializers
from locations_app.models import Cemetery, CemeteryPlot
from locations_app.serializers.cemetery_plot_serializers import (CemeteryPlotSerializer, CemeteryPlotListSerializer,
                                                                 CemeteryPlotCreateSerializer,
                                                                 CemeteryPlotRetrieveSerializer,
                                                                 CemeteryPlotUpdateSerializer)
from locations_app.serializers.cemetery_serializers import CemeterySerializer, CemeteryListSerializer, \
    CemeteryCreateSerializer, CemeteryRetrieveSerializer, CemeteryUpdateSerializer, CemeteryMapSerializer
from django.db.models import Count, Case, When, IntegerField


# Create your views here.
class CemeteryViewSet(CustomModelViewSet):
    queryset = Cemetery.objects.all()
    serializer_class = CemeterySerializer
    filterset_class = CemeteryFilter

    serializer_list = {
        'list': CemeteryListSerializer,
        'create': CemeteryCreateSerializer,
        'update': CemeteryUpdateSerializer,
        'retrieve': CemeteryRetrieveSerializer,
        'public': CemeteryRetrieveSerializer,
        'map': CemeteryMapSerializer,
        'filter_map': CemeteryMapFilterSerializer,
        'filter': CemeteryFilterSerializer,
    }

    permission_classes = [permissions.AllowAny]

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
        return queryset.order_by('id')

    def list(self, request, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = CemeteryListSerializer(page, many=True) if page else CemeteryListSerializer(queryset, many=True)

        return self.get_paginated_response(serializer.data) if page else Response(serializer.data,
                                                                                  status=status.HTTP_200_OK)

    @action(detail=True, methods=['GET'])
    def map(self, request, pk=None):
        cemetery = self.get_object()
        serializer = CemeteryMapSerializer(cemetery, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['GET'])
    def count(self, request, pk=None):
        cemetery = self.get_object()
        serializer = CemeteryMapSerializer(cemetery, context={'request': request})
        serializer_data = serializer.data
        count_of_plots_in_visible_area = len(serializer_data.get('cemetery_plots', []))
        return Response({'count': count_of_plots_in_visible_area}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], permission_classes=[permissions.AllowAny])
    def public(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class CemeteryPlotViewSet(CustomModelViewSet):
    queryset = CemeteryPlot.objects.all()
    serializer_class = CemeteryPlotSerializer
    filterset_class = CemeteryPlotFilter
    serializer_list = {
        'list': CemeteryPlotListSerializer,
        'create': CemeteryPlotCreateSerializer,
        'update': CemeteryPlotUpdateSerializer,
        'retrieve': CemeteryPlotRetrieveSerializer,
        'public': CemeteryPlotRetrieveSerializer,
        'filter': CemeteryPlotFilterSerializers
    }

    permission_classes = [permissions.AllowAny]

    def list(self, request, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).order_by('-id')
        page = self.paginate_queryset(queryset)
        serializer = CemeteryPlotListSerializer(page, many=True) if page else CemeteryPlotListSerializer(queryset,
                                                                                                         many=True)
        return self.get_paginated_response(serializer.data) if page else Response(serializer.data,
                                                                                  status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes=[permissions.AllowAny])
    def public(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
