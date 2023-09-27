# Generated by Django 4.2 on 2023-09-14 10:37

import bboard.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0008_revrubric'),
    ]

    operations = [
        migrations.CreateModel(
            name='Img',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to=bboard.models.get_timestamp_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'jpg'])], verbose_name='Изображение')),
                ('desc', models.TextField(verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Изображение',
                'verbose_name_plural': 'Изображения',
            },
        ),
    ]
