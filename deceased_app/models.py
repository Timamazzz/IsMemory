from django.db import models
from locations_app.models import CemeteryPlot
from users_app.models import CustomUser


# Create your models here.
class Deceased(models.Model):
    cemetery_plot = models.ForeignKey(CemeteryPlot, null=True, blank=True, on_delete=models.CASCADE,
                                      related_name='cemetery_plot_set', verbose_name='Кладбище')
    birth_date = models.DateField("Дата рождения", null=True, blank=True)
    death_date = models.DateField("Дата смерти", null=True, blank=True)
    burial_date = models.DateField("Дата захоронения", null=True, blank=True)

    first_name = models.CharField("Имя", max_length=255, null=True, blank=True)
    last_name = models.CharField("Фамилия", max_length=255, null=True, blank=True)
    patronymic = models.CharField("Отчество", max_length=255, null=True, blank=True)

    notes = models.TextField("Примечание", null=True, blank=True)

    favourites = models.ManyToManyField(CustomUser, related_name='favourites', null=True, blank=True,
                                        verbose_name='В избранном у пользователей')

    class Meta:
        verbose_name = 'Усопший'
        verbose_name_plural = 'Усопшие'
        app_label = 'deceased_app'

    def __str__(self):
        if self.first_name or self.last_name or self.patronymic:
            return f"{self.first_name or ''} {self.last_name or ''} {self.patronymic or ''}".strip()
        else:
            return 'Усопший без имени, но с добрым сердцем'
