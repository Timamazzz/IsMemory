from django.contrib import admin

from docs_app.models import OrderImage
from .models import Executor, Order


@admin.register(Executor)
class ExecutorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'patronymic', 'phone_number')
    search_fields = ('first_name', 'last_name', 'patronymic', 'phone_number')


class OrderImageInline(admin.TabularInline):
    model = OrderImage
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('deceased',)
    list_display = ('date', 'executor', 'service', 'is_good', 'is_bad', 'status')
    inlines = [OrderImageInline]
    list_filter = ('date', 'service', 'is_good', 'is_bad', 'status')



