from django.urls import path, include
from rest_framework.routers import DefaultRouter

from deceased_app.views import DeceasedViewSet

router = DefaultRouter()
router.register(r'', DeceasedViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
