from datetime import datetime
from os.path import splitext

from django.contrib.auth.models import User
from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models
from precise_bbcode.fields import BBCodeTextField


class RubricQuerySet(models.QuerySet):
    def order_by_bb_count(self):
        return self.annotate(cnt=models.Count('bb')).order_by('-cnt')


class RubricManager(models.Manager):
    def get_queryset(self):
        # return super().get_queryset().order_by('name')
        return RubricQuerySet(self.model, using=self._db)

    def order_by_bb_count(self):
        # return super().get_queryset().annotate(cnt=models.Count('bb')).order_by('-cnt')

        return self.get_queryset().order_by_bb_count()


class BbManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('price')


def get_timestamp_path(instance, filename):
    return '%s%s%s' % (splitext(filename)[0], datetime.now().timestamp(), splitext(filename)[1])


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
#     is_activated = models.BooleanField(default=True)
#     user = models.OneToOneField(User, on_delete=models.CASCADE)


# class Spare(models.Model):
#     name = models.CharField(max_length=30)


# class Machine(models.Model):
#     name = models.CharField(max_length=30)
#     spares = models.ManyToManyField(Spare)


class Rubric(models.Model):
    name = models.CharField(max_length=20, db_index=True, verbose_name="Название",)
    objects = RubricManager()
    # objects = RubricQuerySet.as_manager()
    # objects = models.Manager.from_queryset(RubricQuerySet)()

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
    KINDS = (('b', 'Куплю'), ('s', 'Продам'), ('c', 'Поменяю'))
    rubric = models.ForeignKey('Rubric', null=True, on_delete=models.PROTECT, verbose_name='Рубрика',)
    title = models.CharField(max_length=50, verbose_name="Товар", validators=[validators.MinLengthValidator(get_min_length)], error_messages={'min_length': 'Слишком мало символов'})
    kind = models.CharField(max_length=1, choices=KINDS, default='s')
    content = BBCodeTextField(null=True, blank=True, verbose_name="Описание")
    price = models.FloatField(null=True, blank=True, verbose_name="Цена")  # validators=[validate_even, MinMaxValidator(2, 5)]
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Опубликовано")
    archive = models.FileField(upload_to=get_timestamp_path, blank=True)

    objects = models.Manager()
    by_price = BbManager()

    def __str__(self):
        return f'Объявление: {self.title}'

    def title_and_price(self):
        if self.price:
            return f'{self.title} ({self.price:.2f})'
        return self.title

    class Meta:
        # order_with_respect_to = 'rubric'
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ['-published', 'title']


class Human(models.Model):

    floors = [('m', 'man'), ('w', 'woman')]
    name = models.CharField(max_length=20, verbose_name='Имя', blank=False)
    floor = models.CharField(max_length=1, choices=floors, default='m')
    years = models.PositiveSmallIntegerField(verbose_name='Лет')


class Child(models.Model):
    name = models.CharField(max_length=20, verbose_name='Имя', blank=False)
    years = models.PositiveSmallIntegerField(verbose_name='Лет')


class IceCream(models.Model):
    taste = models.CharField(max_length=20, verbose_name='Вкус')


class IceCreamMarket(models.Model):
    name = models.CharField(max_length=20, verbose_name='Название')
