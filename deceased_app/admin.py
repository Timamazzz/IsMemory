from django.contrib import admin

from deceased_app.models import Deceased


# Register your models here.
class DeceasedAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'patronymic', 'birth_date', 'death_date', 'burial_date', 'cemetery_plot')
    search_fields = ('first_name', 'last_name', 'patronymic')
    list_filter = ('death_date', 'burial_date')
    date_hierarchy = 'death_date'


admin.site.register(Deceased, DeceasedAdmin)
