# Generated by Django 4.2 on 2023-05-24 11:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bboard', '0007_alter_bb_order_with_respect_to'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bb',
            options={'ordering': ['-published', 'title'], 'verbose_name': 'Объявление', 'verbose_name_plural': 'Объявления'},
        ),
    ]
