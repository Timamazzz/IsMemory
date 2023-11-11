from django.db import models


# Create your models here.
class Organization(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название организации", blank=True, null=True, )

    class Meta:
        verbose_name = "Организация"
        verbose_name_plural = "Организации"


class CustomUser(AbstractUser):
    patronymic = models.CharField(max_length=30, blank=True, null=True, verbose_name="Отчество")
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, blank=True, null=True,
                                     verbose_name="Организация")

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
        app_label = 'main_app'

    def __str__(self):
        return self.name or "Название"


class CemeteryDoc(models.Model):
    cemetery = models.ForeignKey(Cemetery, null=True, blank=True,
                                 related_name='', on_delete=models.CASCADE)
    file = models.FileField("Файл договора", null=True, blank=True)
    uploaded_at = models.DateTimeField("Дата загрузки", auto_now_add=True, null=True,
                                       blank=True)
    original_name = models.CharField("Оригинальное имя", max_length=255, null=True, blank=True)

    class Meta:
        app_label = 'main_app'
        verbose_name = "Файл кладбища"
        verbose_name_plural = "Файлы кладбища"

    def __str__(self):
        return self.file.url or "Файл к кладбищу"


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
        return str(self.cadastral) if self.cadastral is not None else ''


class CemeteryPlotDoc(models.Model):
    cemetery_plot = models.ForeignKey(CemeteryPlot, null=True, blank=True, on_delete=models.CASCADE)
    file = models.FileField("Файл договора", null=True, blank=True)
    uploaded_at = models.DateTimeField("Дата загрузки", auto_now_add=True, null=True,
                                       blank=True)
    original_name = models.CharField("Оригинальное имя", max_length=255, null=True, blank=True)

    class Meta:
        app_label = 'main_app'
        verbose_name = "Файл участка кладбища"
        verbose_name_plural = "Файлы участка кладбища"

    def __str__(self):
        return self.file.url or "Файл к участку кладбища"


class Deceased(models.Model):
    cemetery_plot = models.ForeignKey(CemeteryPlot, null=True, blank=True, on_delete=models.CASCADE)
    birth_date = models.DateField("Дата рождения", null=True, blank=True)
    death_date = models.DateField("Дата смерти", null=True, blank=True)
    burial_date = models.DateField("Дата захоронения", null=True, blank=True)

    first_name = models.CharField("Имя", max_length=255, null=True, blank=True)
    last_name = models.CharField("Фамилия", max_length=255, null=True, blank=True)
    patronymic = models.CharField("Отчество", max_length=255, null=True, blank=True)

    notes = models.TextField("Примечание", null=True, blank=True)

    class Meta:
        verbose_name = 'Усопший'
        verbose_name_plural = 'Усопшие'
        app_label = 'main_app'

    def __str__(self):
        return self.org_name or "%s %s" % (
            self.fio, defaultfilters.date(self.birth_date, "d.m.Y") if self.birth_date else "") or "Контрагент"