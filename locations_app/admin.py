from django.contrib import admin

from locations_app.models import Municipality, Cemetery


# Register your models here.
class MunicipalityAdmin(admin.ModelAdmin):
    list_display = ('name', 'coordinates')
    search_fields = ('name',)
    list_filter = ('name',)


class CemeteryAdmin(admin.ModelAdmin):
    list_display = ('name', 'municipality', 'date_start', 'date_end', 'status')
    search_fields = ('name', 'municipality__name')
    list_filter = ('municipality', 'status', 'date_start', 'date_end')
    date_hierarchy = 'date_start'


admin.site.register(Municipality, MunicipalityAdmin)
admin.site.register(Cemetery, CemeteryAdmin)
