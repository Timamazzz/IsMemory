from django.contrib import admin

from plots_app.models import CemeteryPlot


# Register your models here.
class CemeteryPlotAdmin(admin.ModelAdmin):
    list_display = ('plot_number', 'cemetery', 'type', 'status')
    search_fields = ('plot_number', 'cemetery__name')
    list_filter = ('cemetery', 'type', 'status')


admin.site.register(CemeteryPlot, CemeteryPlotAdmin)
