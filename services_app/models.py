from django.db import models


# Create your models here.
class Service(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название услуги')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    description = models.TextField(verbose_name='Описание')

    is_multiple_price = models.BooleanField(default=False, verbose_name='Множественная цена')
    count = models.PositiveIntegerField(default=1, verbose_name='Количество')

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    def __str__(self):
        return self.name
