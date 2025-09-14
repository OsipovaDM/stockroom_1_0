# models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import (
    MinValueValidator, MaxValueValidator, RegexValidator)
from django.core.exceptions import ValidationError
from django.utils import timezone


class BaseModel(models.Model):
    is_active = models.BooleanField('Активно', default=True)
    created_at = models.DateTimeField('Добавлено', auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )

    class Meta:
        abstract = True


class Cell(BaseModel):
    """
    Ячейка
    """
    SIZE_CHOICES = [
        ('small', 'Базовый'),
        ('medium', 'Классический'),
        ('large', 'Расширенный'),
    ]

    number = models.CharField('Номер', max_length=4, unique=True, validators=[RegexValidator(regex=r'^[A-Z]{2}\d{2}$')], help_text='Формат: ZZ00')
    size = models.CharField('Размер', max_length=6, choices=SIZE_CHOICES)

    def __str__(self):
        return self.number


# class Tariff(models.Model):
#     """
#     Тариф
#     """
#     name = models.CharField('Название', max_length=255)
#     cell_size = models.CharField('Размер ячейки', max_length=6, choices=Cell.SIZE_CHOICES)
#     duration = models.PositiveIntegerField('Длительность (дней)')
#     cost = models.DecimalField('Стоимость', max_digits=10, decimal_places=2)
#     is_active = models.BooleanField('Активен', default=True)

#     def clean(self):
#         if self.cost <= 0:
#             raise ValidationError('Стоимость должна быть положительна.')

#     def __str__(self):
#         return self.name


# class Promotion(models.Model):
#     """
#     Акция
#     """
#     PROMOTION_TYPES = [
#         ('general', 'Общая'),
#         ('personal', 'Персональная'),
#     ]

#     name = models.CharField('Название', max_length=255)
#     discount_percentage = models.DecimalField(
#         'Скидка в долях', max_digits=5, decimal_places=4, validators=[MinValueValidator(0), MaxValueValidator(1)])
#     start_date = models.DateField('Начало')
#     end_date = models.DateField('Окончание')
#     description = models.TextField('Описание')
#     promotion_type = models.CharField('Тип акции', max_length=10, choices=PROMOTION_TYPES, default='general')
#     target_user = models.ForeignKey(
#         User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Целевой пользователь')
#     is_active = models.BooleanField('Активна', default=True)

#     def clean(self):
#         if self.start_date >= self.end_date:
#             raise ValidationError('Дата начала должна быть раньше даты окончания.')
#         if self.promotion_type == 'personal' and not self.target_user:
#             raise ValidationError('Для персональной акции должен быть указан целевой пользователь.')
#         if not self.promotion_type == 'personal' and self.target_user:
#             raise ValidationError('Для общей акции не должен быть указан целевой пользователь.')

#     def __str__(self):
#         return self.name


# class Order(models.Model):
#     """
#     Заказ
#     """
#     STATUS_CHOICES = [
#         ('pending', 'Ожидает'),
#         ('active', 'Активен'),
#         ('completed', 'Завершен'),
#         ('cancelled', 'Отменен'),
#     ]
    
#     client = models.ForeignKey(User, on_delete=models.CASCADE)
#     cell = models.ForeignKey(Cell, on_delete=models.CASCADE)
#     tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE)
#     promotion = models.ForeignKey(Promotion, on_delete=models.SET_NULL, null=True, blank=True)
#     rental_duration = models.PositiveIntegerField('Длительность (дней)')
#     total_cost = models.DecimalField('Стоимость', max_digits=10, decimal_places=2)
#     rental_start_date = models.DateField('Начало аренды')
#     rental_end_date = models.DateField('Окончание аренды')
#     content_description = models.TextField('Описание содержимого')
#     status = models.CharField('Статус', max_length=10, choices=STATUS_CHOICES, default='pending')
#     created_at = models.DateTimeField('Создан', auto_now_add=True)
#     updated_at = models.DateTimeField('Обновлен', auto_now=True)

#     def clean(self):
#         if self.rental_start_date >= self.rental_end_date:
#             raise ValidationError('Дата начала должна быть раньше даты окончания.')
#         if self.cell.size != self.tariff.cell_size:
#             raise ValidationError('Размер ячейки должен соответствовать размеру тарифа.')
#         if self.rental_duration % self.tariff.duration != 0:
#             raise ValidationError('Длительность заказа должна быть кратна продолжительности тарифа.')
#         overlapping_orders = Order.objects.filter(cell=self.cell, start_date__lt=self.end_date, end_date__gt=self.start_date)
#         if overlapping_orders.exists():
#             raise ValidationError('На выбранные даты ячейка уже занята.')

#     def save(self, *args, **kwargs):
#         # Автоматический расчет стоимости
#         if not self.total_cost:
#             base_cost = self.tariff.cost * (self.rental_duration / self.tariff.duration)
#             if self.promotion:
#                 discount = base_cost * self.promotion.discount_percentage
#                 self.total_cost = base_cost - discount
#             else:
#                 self.total_cost = base_cost

#         # Автоматическое обновление статуса
#         today = timezone.now().date()
#         if self.status != 'cancelled':
#             if today < self.rental_start_date:
#                 self.status = 'pending'
#             elif self.rental_start_date <= today <= self.rental_end_date:
#                 self.status = 'active'
#             elif today > self.rental_end_date:
#                 self.status = 'completed'

#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f'{self.cell.number} - {self.client.username}'
    