from django.db import models


# Create your models here.
class CustomUser(AbstractUser):
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username


class Municipality(models.Model):
    name = models.CharField("Название", max_length=255, null=True, blank=True)
    coordinates = models.JSONField("Координаты", null=True, blank=True)

    class Meta:
        verbose_name = 'Муниципальное образование'
        verbose_name_plural = 'Муниципальные образования'
        app_label = 'main_app'

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

    system_status = models.JSONField(
        default=list,
        verbose_name="Статус в системе",
        null=True,
        blank=True,
        choices=[(status.name, status.value) for status in SystemStatusMicrodistrictEnum],
    )

    is_gas_supply = models.BooleanField("Газоснабжение", default=False, null=True, blank=True)
    gas_supply_building_status = models.CharField(
        "Статус строительства",
        max_length=255,
        choices=[(status.name, status.value) for status in BuildingStatusEnum],
        null=True,
        blank=True
    )
    gas_supply_date_end = models.DateField("Дата завершения", null=True, blank=True)

    is_water_supply = models.BooleanField("Водоснабжение и водоотведение", default=False, null=True, blank=True)
    water_supply_building_status = models.CharField(
        "Статус строительства",
        max_length=255,
        choices=[(status.name, status.value) for status in BuildingStatusEnum],
        null=True,
        blank=True
    )
    water_supply_date_end = models.DateField("Дата завершения", null=True, blank=True)

    sanitation = models.CharField(
        "Водоотведение",
        max_length=255,
        choices=[(sanitation.name, sanitation.value) for sanitation in SanitationEnum],
        null=True,
        blank=True
    )

    property = models.CharField("Собственность", max_length=255,
                                choices=[(property.name, property.value) for property in PropertyEnum],
                                null=True, blank=True)

    is_power_supply = models.BooleanField("Электроснабжение", default=False, null=True, blank=True)
    power_supply_building_status = models.CharField(
        "Статус строительства",
        max_length=255,
        choices=[(status.name, status.value) for status in BuildingStatusEnum],
        null=True,
        blank=True
    )
    power_supply_date_end = models.DateField("Дата завершения", null=True, blank=True)

    is_road_surface = models.BooleanField("Дорожное покрытие", default=False, null=True, blank=True)
    road_surface_building_status = models.CharField(
        "Статус строительства",
        max_length=255,
        choices=[(status.name, status.value) for status in BuildingStatusEnum],
        null=True,
        blank=True
    )
    road_surface_date_end = models.DateField("Дата завершения", null=True, blank=True)
    road_surface_type = models.CharField(
        "Тип покрытия дороги",
        max_length=255,
        choices=[(surface.name, surface.value) for surface in RoadSurfaceTypeEnum],
        null=True,
        blank=True
    )

    is_social_objects = models.BooleanField("Социальные объекты", default=False, null=True, blank=True)
    is_commercial_objects = models.BooleanField("Коммерческие объекты", default=False, null=True, blank=True)

    class Meta:
        verbose_name = 'Микрорайон'
        verbose_name_plural = 'Микрорайоны'
        app_label = 'main_app'

    def __str__(self):
        return self.name or "Название"
