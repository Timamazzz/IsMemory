from django.urls import path, include
from rest_framework.routers import DefaultRouter

from locations_app.views import CemeteryViewSet

router = DefaultRouter()
router.register(r'cemeteries', CemeteryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
