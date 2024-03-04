from django.urls import path, include
from rest_framework.routers import DefaultRouter

from locations_app.views import CemeteryViewSet, CemeteryPlotViewSet, MapListView

router = DefaultRouter()
router.register(r'cemeteries', CemeteryViewSet)
router.register(r'cemetery-plots', CemeteryPlotViewSet)

urlpatterns = [
    path('cemeteries/map-list/', MapListView.as_view(), name='map-list'),
    path('', include(router.urls)),
]
