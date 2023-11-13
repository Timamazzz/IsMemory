from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users_app import views
from users_app.views import UserViewSet

router = DefaultRouter()
router.register(r'', UserViewSet)

urlpatterns = [

    path('register/', views.register, name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    path('reset-password/', views.reset_password, name='reset_password'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', include(router.urls)),
]
