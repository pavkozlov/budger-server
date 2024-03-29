# Generated by Django 2.2.8 on 2019-12-11 12:43

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0028_auto_20191210_1830'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='initiator',
        ),
        migrations.AddField(
            model_name='event',
            name='initiators',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.PositiveSmallIntegerField(choices=[(1, 'Предложение Губернатора Московской области'), (2, 'Поручение Московской областной думы'), (3, 'Обращение Правительства Московской области / Администрации муниципального образования'), (4, 'Обращение граждан'), (5, 'Обращение общественных организаций'), (6, 'Обращение правоохранительных органов'), (7, 'Решение Совета КСО МО'), (8, 'Решение органа аудита (контроля)')]), blank=True, null=True, size=None),
        ),
    ]
