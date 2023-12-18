from django.urls import path, include
from rest_framework.routers import DefaultRouter
from orders_app.views import OrderViewSet, ExecutorViewSet

router = DefaultRouter()
router.register(r'executors', ExecutorViewSet)
router.register(r'', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
