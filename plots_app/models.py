from django.db import models

from locations_app.models import Cemetery
from plots_app.enums import CemeteryPlotTypeEnum, CemeteryPlotStatusEnum


# Create your models here.
class CemeteryPlot(models.Model):
    # cadastral = models.CharField("Кадастровый номер", max_length=255, null=True, blank=True)
    cemetery = models.ForeignKey(Cemetery, on_delete=models.CASCADE, verbose_name="Кладбище", null=True, blank=True)
    plot_number = models.CharField("Номер участка", max_length=255, null=True, blank=True)
    sector = models.CharField("Сектор", max_length=255, null=True, blank=True)
    row = models.CharField("Ряд", max_length=255, null=True, blank=True)
    burial = models.CharField("Захоронение", max_length=255, null=True, blank=True)
    place = models.CharField("Место", max_length=255, null=True, blank=True)

    coordinates = models.JSONField("Координаты", null=True, blank=True)

    type = models.CharField(
        "Тип",
        max_length=255,
        choices=[(type.name, type.value) for type in CemeteryPlotTypeEnum],
        null=True,
        blank=True
    )

    status = models.CharField(
        "Статус",
        max_length=255,
        choices=[(status.name, status.value) for status in CemeteryPlotStatusEnum],
        null=True,
        blank=True
    )

    # Description
    description = models.TextField("Описание", null=True, blank=True)
    note = models.TextField("Примечание", null=True, blank=True)

    class Meta:
        verbose_name = 'Участок'
        verbose_name_plural = 'Участки'
        app_label = 'main_app'

    def __str__(self):
        return 'Участок'
