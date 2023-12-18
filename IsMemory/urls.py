"""
URL configuration for IsMemory project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve

from IsMemory import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users_app.urls')),
    path('api/deceased/', include('deceased_app.urls')),
    path('api/locations/', include('locations_app.urls')),
    path('api/services/', include('services_app.urls')),
    path('api/orders/', include('orders_app.urls')),
    re_path(r'^media/(?P<path>.*)$', serve,
         {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
]
