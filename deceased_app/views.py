from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.views import APIView

from users_app.admin_permissions import HasDashboardAdminGroupPermission
from IsMemory.helpers.CustomModelViewSet import CustomModelViewSet
from IsMemory.helpers.CustomOptionsMetadata import CustomOptionsMetadata
from deceased_app.filters import DeceasedFilter, DeceasedFilterSerializer
from deceased_app.models import Deceased
from deceased_app.serializers.deceased_serializers import DeceasedSerializer, DeceasedCreateSerializer, \
    DeceasedFavouriteListSerializer, DeceasedFavouriteSerializer
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
    metadata_class = CustomOptionsMetadata

    def get_queryset(self):
        queryset = Deceased.objects.all()
        filterset = self.filterset_class(self.request.query_params, queryset=queryset)
        return filterset.qs

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FavouritesDeceasedViewSet(CustomModelViewSet):
    queryset = Deceased.objects.all()
    serializer_class = DeceasedSerializer
    serializer_list = {
        'list': DeceasedFavouriteListSerializer,
        'favourite': DeceasedFavouriteSerializer,
    }
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, **kwargs):
        user = request.user
        queryset = user.favourites.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def favourite(self, request, pk=None):
        user = request.user
        deceased = get_object_or_404(Deceased, pk=pk)

        if deceased.favourites.filter(id=user.pk).exists():
            deceased.favourites.remove(user)
            message = 'Removed from favorites'
            status_code = status.HTTP_200_OK
        else:
            deceased.favourites.add(user)
            message = 'Added to favorites'
            status_code = status.HTTP_201_CREATED

        return Response({'message': message}, status=status_code)
