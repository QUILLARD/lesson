from django.contrib.auth.models import User
from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models


def get_min_length():
    min_length = 3
    return min_length


def validate_even(val):
    if val % 2 != 0:
        raise ValidationError('Число %(value)s нечётное', code='odd', params={'value': val})


# class MinMaxValidator:
#     def __init__(self, min_value, max_value):
#         self.min_value = min_value
#         self.max_value = max_value
#
#     def __call__(self, val):
#         if val < self.min_value or val > self.max_value:
#             raise ValidationError('Введённое число должно быть > %(min)s и < %(max)s',
#                                   code='out_of_range',
#                                   params={'min': self.min_value,
#                                           'max': self.max_value})


# class AdvUser(models.Model):
#     is_activated = models.BooleanField(
#         default=True,
#     )
#
#     user = models.OneToOneField(
#         User,
#         on_delete=models.CASCADE
#     )


# class Spare(models.Model):
#     name = models.CharField(
#         max_length=30,
#     )


# class Machine(models.Model):
#     name = models.CharField(
#         max_length=30,
#     )
#
#     spares = models.ManyToManyField(
#         Spare,
#     )


class Rubric(models.Model):
    name = models.CharField(
        max_length=20,
        db_index=True,
        verbose_name="Название",)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Выполняем какие-то действия до сохранения
        if True:
            super().save(*args, **kwargs)
        # Выполняем какие-то действия после сохранения

    def delete(self, *args, **kwargs):
        # Выполняем какие-то действия до удаления
        if True:
            super().delete(*args, **kwargs)
        # Выполняем какие-то действия после удаления

    def get_absolute_url(self):
        return f'/{self.pk}/'

    class Meta:
        verbose_name = 'Рубрика'
        verbose_name_plural = 'Рубрики'
        ordering = ['name']


class Bb(models.Model):
    rubric = models.ForeignKey(
        'Rubric',
        null=True,
        on_delete=models.PROTECT,
        verbose_name='Рубрика',
    )

    title = models.CharField(
        max_length=50,
        verbose_name="Товар",
        validators=[validators.MinLengthValidator(get_min_length)],
        error_messages={'min_length': 'Слишком мало символов'},
    )

    content = models.TextField(
        null=True,
        blank=True,
        verbose_name="Описание",
    )

    price = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Цена",
        # validators=[validate_even, MinMaxValidator(2, 5)]
    )

    published = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name="Опубликовано",
    )

    def __str__(self):
        return f'Объявление: {self.title}'

    def title_and_price(self):
        if self.price:
            return f'{self.title} ({self.price:.2f})'
        return self.title

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ['-published', 'title']


class Human(models.Model):

    floors = [
        ('m', 'man'),
        ('w', 'woman'),
    ]

    name = models.CharField(
        max_length=20,
        verbose_name='Имя',
        blank=False,
    )

    floor = models.CharField(
        max_length=1,
        choices=floors,
        default='m',
    )

    years = models.PositiveSmallIntegerField(
        verbose_name='Лет',
    )


class Child(models.Model):
    name = models.CharField(
        max_length=20,
        verbose_name='Имя',
        blank=False,
    )

    years = models.PositiveSmallIntegerField(
        verbose_name='Лет',
    )


class IceCream(models.Model):
    taste = models.CharField(
        max_length=20,
        verbose_name='Вкус',
    )


class IceCreamMarket(models.Model):
    name = models.CharField(
        max_length=20,
        verbose_name='Название',
    )
