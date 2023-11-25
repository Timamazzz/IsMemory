from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions

from IsMemory.helpers.CustomModelViewSet import CustomModelViewSet
from deceased_app.filters import DeceasedFilter
from deceased_app.models import Deceased
from deceased_app.serializers.deceased_serializers import DeceasedSerializer, DeceasedCreateSerializer
from rest_framework import filters


# Create your views here.
class DeceasedViewSet(CustomModelViewSet):
    queryset = Deceased.objects.all()
    serializer_class = DeceasedSerializer
    serializer_list = {
        'retrieve': DeceasedSerializer,
        'create': DeceasedCreateSerializer,
        'filter': DeceasedFilter
    }
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = DeceasedFilter

