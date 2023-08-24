from django.contrib.auth.models import User
from django.db import models


class AdvUser(models.Model):
    is_activated = models.BooleanField(
        default=True,
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )


class Spare(models.Model):
    name = models.CharField(
        max_length=30,
    )


class Machine(models.Model):
    name = models.CharField(
        max_length=30,
    )

    spares = models.ManyToManyField(
        Spare,
        through='Kit',
        through_fields=('machine', 'spare')
    )


class Kit(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    spare = models.ForeignKey(Spare, on_delete=models.CASCADE)
    count = models.IntegerField()


class SMS(models.Model):
    comment = models.CharField(
        max_length=120,
        verbose_name='Комментарий'
    )

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sender',
        verbose_name='Отправитель'
    )

    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='receiver',
        verbose_name='Получатель'
    )

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

