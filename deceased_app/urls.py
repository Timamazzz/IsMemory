from django.urls import path, include
from rest_framework.routers import DefaultRouter

from deceased_app.views import DeceasedViewSet, SearchDeceasedAPIView

router = DefaultRouter()
router.register(r'', DeceasedViewSet)

urlpatterns = [
    path('search-deceased/', SearchDeceasedAPIView.as_view(), name='search_deceased'),
    path('', include(router.urls)),
]
