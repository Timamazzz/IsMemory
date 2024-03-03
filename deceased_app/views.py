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
    DeceasedFavouriteListSerializer, DeceasedFavouriteSerializer, DeceasedListSerializer
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


# Create your views here.
class DeceasedViewSet(CustomModelViewSet):
    queryset = Deceased.objects.all()
    serializer_class = DeceasedSerializer
    serializer_list = {
        'retrieve': DeceasedSerializer,
        'create': DeceasedCreateSerializer,
    }
    pagination_class = PageNumberPagination
    permission_classes = [permissions.AllowAny]


class SearchDeceasedAPIView(APIView):
    queryset = Deceased.objects.all()
    serializer_class = DeceasedSerializer
    serializer_list = {
        'filter': DeceasedFilterSerializer
    }
    filterset_class = DeceasedFilter
    metadata_class = CustomOptionsMetadata
    pagination_class = PageNumberPagination

    def get_queryset(self):
        filterset = self.filterset_class(self.request.query_params, queryset=self.queryset)
        return filterset.qs

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk', None)
        queryset = self.get_queryset()
        if pk:
            deceased = get_object_or_404(queryset, pk=pk)
            serializer = DeceasedSerializer(deceased)
            return Response(serializer.data, status=status.HTTP_200_OK)

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = DeceasedListSerializer(page, many=True, context={'request': self.request})
            return paginator.get_paginated_response(serializer.data)

        serializer = DeceasedListSerializer(queryset, many=True, context={'request': self.request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class FavouritesDeceasedViewSet(CustomModelViewSet):
    queryset = Deceased.objects.all()
    serializer_class = DeceasedSerializer
    serializer_list = {
        'list': DeceasedFavouriteListSerializer,
        'favourite': DeceasedFavouriteSerializer,
    }
    permission_classes = [permissions.AllowAny]

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
        else:
            deceased.favourites.add(user)

        queryset = user.favourites.all()
        serializer = DeceasedFavouriteListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
