from django.contrib import admin

from docs_app.models import CemeteryPlotImage
from locations_app.models import Municipality, Cemetery, CemeteryPlot


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


class CemeteryPlotImageInline(admin.TabularInline):
    model = CemeteryPlotImage
    extra = 3


class CemeteryPlotAdmin(admin.ModelAdmin):
    list_display = ('plot_number', 'cemetery', 'type', 'status')
    search_fields = ('plot_number', 'cemetery__name')
    list_filter = ('cemetery', 'type', 'status')
    inlines = [CemeteryPlotImageInline]


admin.site.register(Municipality, MunicipalityAdmin)
admin.site.register(Cemetery, CemeteryAdmin)
admin.site.register(CemeteryPlot, CemeteryPlotAdmin)
