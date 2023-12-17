from django.db import models
from deceased_app.models import Deceased
from orders_app.enums import OrderStatusEnum
from services_app.models import Service
from users_app.models import PhoneNumberValidator, CustomUser


class Executor(models.Model):
    first_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='Имя исполнителя')
    last_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='Фамилия исполнителя')
    patronymic = models.CharField(max_length=255, null=True, blank=True, verbose_name='Отчество исполнителя')
    phone_number = models.CharField(
        validators=[PhoneNumberValidator()],
        max_length=17,
        unique=True,
        blank=True,
        null=True,
        verbose_name="Номер телефона"
    )

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.patronymic} - {self.phone_number}'

    class Meta:
        verbose_name = 'Исполнитель'
        verbose_name_plural = 'Исполнители'
        app_label = 'orders_app'


class Order(models.Model):
    date = models.DateField(verbose_name='Дата заказа', auto_now_add=True, null=True, blank=True,)

    executor = models.ForeignKey(Executor, on_delete=models.SET_NULL, null=True, blank=True,
                                 verbose_name='Исполнитель')

    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name='Услуга', null=True, blank=True)
    deceased = models.ForeignKey(Deceased, on_delete=models.CASCADE, verbose_name='Усопший', null=True, blank=True)

    comment = models.TextField(blank=True, null=True, verbose_name='Комментарий')
    is_good = models.BooleanField(default=False, verbose_name='Все хорошо')
    is_bad = models.BooleanField(default=False, verbose_name='Есть замечания')

    status = models.CharField(
        max_length=20,
        choices=[(status.name, status.value) for status in OrderStatusEnum],
        default=OrderStatusEnum.AWAITING_PAYMENT.name,
        verbose_name='Статус',
        null=True,
        blank=True
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Пользователь',)

    def __str__(self):
        return f'Заказ №{self.id} {self.date.strftime("%d-%m-%Y")}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        app_label = 'orders_app'
