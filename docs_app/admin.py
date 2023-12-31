from django.contrib import admin

from docs_app.models import CemeteryDoc, CemeteryPlotDoc


# Register your models here.
class CemeteryDocAdmin(admin.ModelAdmin):
    list_display = ('cemetery', 'file', 'uploaded_at', 'original_name')
    search_fields = ('cemetery__name', 'original_name')
    list_filter = ('cemetery',)
    date_hierarchy = 'uploaded_at'


class CemeteryPlotDocAdmin(admin.ModelAdmin):
    list_display = ('cemetery_plot', 'file', 'uploaded_at', 'original_name')
    search_fields = ('cemetery_plot__name', 'original_name')
    list_filter = ('cemetery_plot',)
    date_hierarchy = 'uploaded_at'


admin.site.register(CemeteryDoc, CemeteryDocAdmin)
admin.site.register(CemeteryPlotDoc, CemeteryPlotDocAdmin)
