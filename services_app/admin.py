from django.contrib import admin
from services_app.models import Service


# Register your models here.
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description')
    search_fields = ('name',)


admin.site.register(Service, ServiceAdmin)
