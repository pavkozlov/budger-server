# Generated by Django 2.2.6 on 2019-11-29 09:12

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0015_auto_20191128_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='initiator',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Предложение Губернатора Московской области'), (2, 'Поручение Московской областной думы'), (3, 'Обращение гражданина'), (4, 'Обращение общественной организации'), (5, 'Обращение правоохранительных органов'), (6, 'Решение Совета КСО МО'), (7, 'Решение органа аудита (контроля)'), (8, 'Обращение Правительства Московской области')], null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='subject',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.PositiveSmallIntegerField(choices=[(1, 'Финансовый аудит (контроль)'), (2, 'Аудит в сфере закупок'), (3, 'Аудит эффективности'), (4, 'Экспертиза проекта закона'), (5, 'Финансово-экономическая экспертиза')]), blank=True, default=None, null=True, size=3),
        ),
        migrations.AlterField(
            model_name='event',
            name='subtype',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.PositiveSmallIntegerField(choices=[(1, 'Оценка рисков возникновения коррупционных проявлений'), (2, 'Проверка реализации приоритетных и национальных проектов'), (3, 'Проверка соблюдения порядка управления и распоряжения имуществом'), (4, 'Проверка порядка и условий предоставления межбюджетных трансфертов')]), blank=True, null=True, size=None),
        ),
    ]
