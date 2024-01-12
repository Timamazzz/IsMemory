from django.db import models
from locations_app.models import Cemetery, CemeteryPlot
from orders_app.models import Order


# Create your models here.
class CemeteryPlotImage(models.Model):
    cemetery_plot = models.ForeignKey(CemeteryPlot, null=True, blank=True, on_delete=models.CASCADE)
    file = models.FileField("Изображение участка", null=True, blank=True)
    uploaded_at = models.DateTimeField("Дата загрузки", auto_now_add=True, null=True,
                                       blank=True)
    original_name = models.CharField("Оригинальное имя", max_length=255, null=True, blank=True)
    is_preview = models.BooleanField("Главное изображение", default=False, null=True, blank=True)

    class Meta:
        app_label = 'docs_app'
        verbose_name = "Изображение участка кладбища"
        verbose_name_plural = "Изображения участка кладбища"

    def __str__(self):
        return self.file.url or "Изображение участка кладбища"


class OrderImage(models.Model):
    Order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.CASCADE, related_name='images_order_rel')
    file = models.FileField("Изображение", null=True, blank=True)
    uploaded_at = models.DateTimeField("Дата загрузки",  null=True,
                                       blank=True, auto_now=True)
    original_name = models.CharField("Оригинальное имя", max_length=255, null=True, blank=True)

    class Meta:
        app_label = 'docs_app'
        verbose_name = "Изображение окончание работы"
        verbose_name_plural = "Изображения окончание работы"

    def __str__(self):
        return self.file.url or "Изображение окончание работы"
