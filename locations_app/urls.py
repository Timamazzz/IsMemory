from django.urls import path, include
from rest_framework.routers import DefaultRouter

from locations_app.views import CemeteryViewSet, CemeteryPlotViewSet

router = DefaultRouter()
router.register(r'cemeteries', CemeteryViewSet)
router.register(r'cemetery-plots', CemeteryPlotViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
