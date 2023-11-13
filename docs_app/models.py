from django.db import models
from locations_app.models import Cemetery, CemeteryPlot


# Create your models here.
class CemeteryDoc(models.Model):
    cemetery = models.ForeignKey(Cemetery, null=True, blank=True, on_delete=models.CASCADE)
    file = models.FileField("Файл договора", null=True, blank=True)
    uploaded_at = models.DateTimeField("Дата загрузки", auto_now_add=True, null=True,
                                       blank=True)
    original_name = models.CharField("Оригинальное имя", max_length=255, null=True, blank=True)

    class Meta:
        app_label = 'docs_app'
        verbose_name = "Файл кладбища"
        verbose_name_plural = "Файлы кладбища"

    def __str__(self):
        return self.file.url or "Файл к кладбищу"


class CemeteryPlotDoc(models.Model):
    cemetery_plot = models.ForeignKey(CemeteryPlot, null=True, blank=True, on_delete=models.CASCADE)
    file = models.FileField("Файл договора", null=True, blank=True)
    uploaded_at = models.DateTimeField("Дата загрузки", auto_now_add=True, null=True,
                                       blank=True)
    original_name = models.CharField("Оригинальное имя", max_length=255, null=True, blank=True)

    class Meta:
        app_label = 'docs_app'
        verbose_name = "Файл участка кладбища"
        verbose_name_plural = "Файлы участка кладбища"

    def __str__(self):
        return self.file.url or "Файл к участку кладбища"
