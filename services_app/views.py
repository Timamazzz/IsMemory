from rest_framework import permissions

from IsMemory.helpers.CustomModelViewSet import CustomModelViewSet
from services_app.models import Service
from services_app.serializers.service_serializers import ServiceListSerializer, ServiceSerializer


# Create your views here.
class ServiceViewSet(CustomModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    serializer_list = {
        'list': ServiceListSerializer,
    }
    #permission_classes = [permissions.IsAuthenticated]