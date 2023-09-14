from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.validators import FileExtensionValidator
from django.db import models

from bboard.models import Rubric, get_timestamp_path


class AdvUser(models.Model):
    is_activated = models.BooleanField(default=True, )
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Spare(models.Model):
    name = models.CharField(max_length=30, )


class Machine(models.Model):
    name = models.CharField(max_length=30, )
    spares = models.ManyToManyField(Spare, through='Kit', through_fields=('machine', 'spare'))
    notes = GenericRelation('Note')


class Kit(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    spare = models.ForeignKey(Spare, on_delete=models.CASCADE)
    count = models.IntegerField()


class SMS(models.Model):
    comment = models.CharField(max_length=120, verbose_name='Комментарий')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender', verbose_name='Отправитель')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver', verbose_name='Получатель')

    def __str__(self):
        return self.comment

    class Meta:
        verbose_name = 'SMS'
        verbose_name_plural = 'SMS'


class Course(models.Model):
    name = models.CharField(max_length=255)


class Student(models.Model):
    name = models.CharField(max_length=100)
    courses = models.ManyToManyField(Course, through='Registration', through_fields=('student', 'course'))


class Registration(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateTimeField()


class Note(models.Model):
    content = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(ct_field='content_type', fk_field='object_id')


# Прямое наследование
# class Message(models.Model):
#     content = models.TextField()
#
#
# class PrivateMessage(Message):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     message = models.OneToOneField(Message, on_delete=models.CASCADE, parent_link=True)


# Абстрактные модели

class Message(models.Model):
    content = models.TextField()
    name = models.CharField(max_length=20)
    email = models.EmailField()

    class Meta:
        abstract = True
        ordering = ['name']


class PrivateMessage(Message):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    email = None


# Прокси-Модели

class RevRubric(Rubric):
    class Meta:
        proxy = True
        ordering = ['-name']


class Img(models.Model):
    img = models.ImageField(upload_to=get_timestamp_path, verbose_name='Изображение', validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'png'])])
    desc = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
