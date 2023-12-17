from django.contrib import admin
from .models import Executor, Order


@admin.register(Executor)
class ExecutorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'patronymic', 'phone_number')
    search_fields = ('first_name', 'last_name', 'patronymic', 'phone_number')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('date', 'executor', 'service', 'deceased', 'is_good', 'is_bad', 'status')
