from django.contrib import admin

from docs_app.models import CemeteryPlotImage


# Register your models here.
class CemeteryPlotImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'cemetery_plot', 'file', 'uploaded_at', 'original_name', 'is_preview')
    search_fields = ('cemetery_plot__name', 'original_name')
    list_filter = ('cemetery_plot',)
    date_hierarchy = 'uploaded_at'


admin.site.register(CemeteryPlotImage, CemeteryPlotImageAdmin)
