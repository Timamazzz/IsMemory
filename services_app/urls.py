from django.urls import path, include
from rest_framework.routers import DefaultRouter
from services_app.views import ServiceViewSet

router = DefaultRouter()
router.register(r'', ServiceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
