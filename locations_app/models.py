from django.db import models
from locations_app.enums import CemeteryStatusEnum, CemeteryPlotTypeEnum, CemeteryPlotStatusEnum


# Create your models here.
class Municipality(models.Model):
    name = models.CharField("Название", max_length=255, null=True, blank=True)
    coordinates = models.JSONField("Координаты", null=True, blank=True)

    class Meta:
        verbose_name = 'Муниципальное образование'
        verbose_name_plural = 'Муниципальные образования'
        app_label = 'locations_app'

    def __str__(self):
        return self.name or "Название"


class Cemetery(models.Model):
    name = models.CharField("Название кладбища", max_length=255, null=True, blank=True)
    coordinates = models.JSONField("Координаты", null=True, blank=True)
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, verbose_name="Муниципальное образование",
                                     null=True, blank=True)
    date_start = models.DateField("Дата освоения", null=True, blank=True)
    date_end = models.DateField("План завершения", null=True, blank=True)
    description = models.CharField("Описание", max_length=255, null=True, blank=True)
    area = models.CharField("Площадь", max_length=255, null=True, blank=True)

    status = models.CharField(
        "Статус",
        max_length=255,
        choices=[(status.name, status.value) for status in CemeteryStatusEnum],
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Кладбище'
        verbose_name_plural = 'Кладбища'
        app_label = 'locations_app'

    def __str__(self):
        return self.name or "Название"


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
        app_label = 'locations_app'

    def __str__(self):
        return 'Участок'