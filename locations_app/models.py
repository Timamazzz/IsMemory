from django.db import models
from locations_app.enums import CemeteryStatusEnum


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
