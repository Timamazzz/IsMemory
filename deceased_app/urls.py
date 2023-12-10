from django.urls import path, include
from rest_framework.routers import DefaultRouter

from deceased_app.views import DeceasedViewSet, SearchDeceasedAPIView, FavouritesDeceasedViewSet

router = DefaultRouter()
router.register(r'favourites', FavouritesDeceasedViewSet)
router.register(r'', DeceasedViewSet)

urlpatterns = [
    path('search-deceased/<int:pk>', SearchDeceasedAPIView.as_view(), name='search_deceased'),
    path('', include(router.urls)),
]
