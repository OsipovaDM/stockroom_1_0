from django.db import models
from django.contrib.auth.models import User
from django.core.validators import (
    MinValueValidator, MaxValueValidator, RegexValidator)
from django.core.exceptions import ValidationError


SIZE_CHOICES = [
        ('small', 'Базовый'),
        ('medium', 'Классический'),
        ('large', 'Расширенный'),
    ]


class Cell(models.Model):
    """
    Ячейка
    """
    number = models.CharField('Номер', max_length=4, unique=True, validators=[RegexValidator(regex=r'^[A-Z]{2}\d{2}$')])
    size = models.CharField('Размер', max_length=6, choices=SIZE_CHOICES)

    def __str__(self):
        return self.number


class Tariff(models.Model):
    """
    Тариф
    """
    name = models.CharField('Название', max_length=255)
    cell_size = models.CharField('Размер ячейки', max_length=6, choices=SIZE_CHOICES)
    duration = models.PositiveIntegerField('Длительность', )  # Длительность тарифа в сутках
    cost = models.DecimalField('Стоимость', max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Promotion(models.Model):
    """
    Акция
    """
    name = models.CharField('Название', max_length=255)
    discount_percentage = models.DecimalField('Скидка в долях', max_digits=5, decimal_places=4, validators=[MinValueValidator(0), MaxValueValidator(1)])
    start_date = models.DateField('Начало', )
    end_date = models.DateField('Окончание', )
    description = models.TextField('Описание', )

    def clean(self):  # Позже реализовать проверку на уровне форм
        if self.start_date >= self.end_date:
            raise ValidationError('Start date must be before end date.')

    def __str__(self):
        return self.name


class Order(models.Model):
    """
    Заказ
    """
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    cell = models.ForeignKey(Cell, on_delete=models.CASCADE)
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE)
    promotion = models.ForeignKey(Promotion, on_delete=models.SET_NULL, null=True, blank=True)
    rental_duration = models.PositiveIntegerField('Длительность', )  # Длительность аренды в сутках
    total_cost = models.DecimalField('Стоимость', max_digits=10, decimal_places=2)
    rental_start_date = models.DateField('Начало', )
    rental_end_date = models.DateField('Окончание', )
    content_description = models.TextField('Перепись содержимого', )

    def clean(self):  # Позже реализовать проверку на уровне форм
        if self.start_date >= self.end_date:
            raise ValidationError('Start date must be before end date.')
        if self.cell.size != self.tariff.cell_size:
            raise ValidationError('Cell size must match the tariff size.')
        if self.rental_duration % self.tariff.duration != 0:
            raise ValidationError('Rental duration must be a multiple of the tariff period.')
        overlapping_orders = Order.objects.filter(cell=self.cell, start_date__lt=self.end_date, end_date__gt=self.start_date)
        if overlapping_orders.exists():
            raise ValidationError('There is an overlapping order for this cell.')

    def __str__(self):
        return f'{self.cell.number} {self.rental_end_date}'
