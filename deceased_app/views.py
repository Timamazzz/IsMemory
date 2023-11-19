from django.shortcuts import render
from rest_framework import permissions

from IsMemory.helpers.CustomModelViewSet import CustomModelViewSet
from deceased_app.models import Deceased
from deceased_app.serializers.deceased_serializers import DeceasedSerializer


# Create your views here.
class DeceasedViewSet(CustomModelViewSet):
    queryset = Deceased.objects.all()
    serializer_class = DeceasedSerializer
    serializer_list = {
        'retrieve': DeceasedSerializer,
    }
    permission_classes = [permissions.IsAuthenticated]

