from django.contrib.auth.models import AbstractUser
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
