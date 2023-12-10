from rest_framework import permissions, status
from rest_framework.views import APIView

from IsMemory.admin_permissions import HasDashboardAdminGroupPermission
from IsMemory.helpers.CustomModelViewSet import CustomModelViewSet
from deceased_app.filters import DeceasedFilter, DeceasedFilterSerializer
from deceased_app.models import Deceased
from deceased_app.serializers.deceased_serializers import DeceasedSerializer, DeceasedCreateSerializer
from rest_framework.response import Response


# Create your views here.
class DeceasedViewSet(CustomModelViewSet):
    queryset = Deceased.objects.all()
    serializer_class = DeceasedSerializer
    serializer_list = {
        'retrieve': DeceasedSerializer,
        'create': DeceasedCreateSerializer,
    }
    permission_classes = [permissions.IsAuthenticated, HasDashboardAdminGroupPermission]


class SearchDeceasedAPIView(APIView):
    queryset = Deceased.objects.all()
    serializer_class = DeceasedSerializer
    serializer_list = {
        'filter': DeceasedFilterSerializer
    }
    filterset_class = DeceasedFilter

    def get_queryset(self):
        queryset = Deceased.objects.all()
        filterset = self.filterset_class(self.request.query_params, queryset=queryset)
        return filterset.qs

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

