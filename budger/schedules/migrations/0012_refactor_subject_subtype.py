# Generated by Django 2.2.6 on 2019-11-25 11:01

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0011_enums_refactored'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='subject_financial',
        ),
        migrations.RemoveField(
            model_name='event',
            name='subject_performance',
        ),
        migrations.AlterField(
            model_name='event',
            name='subject',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.PositiveSmallIntegerField(choices=[(1, 'Финансовый аудит (контроль)'), (2, 'Аудит в сфере закупок'), (3, 'Аудит эффективности'), (4, 'Экспертиза проекта закона'), (5, 'Финансово-экономическая экспертиза')]), blank=True, default=None, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='event',
            name='subtype',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.PositiveSmallIntegerField(choices=[(1, 'С оценкой рисков возникновения коррупционных проявлений'), (2, 'С проверкой реализации приоритетных и национальных проектов'), (3, 'С проверкой соблюдения порядка управления и распоряжения имуществом'), (4, 'С проверкой порядка и условий предоставления межбюджетных трансфертов')]), blank=True, null=True, size=None),
        ),
        migrations.RemoveField(
            model_name='event',
            name='subtype',
        ),
        migrations.AddField(
            model_name='event',
            name='subtype',
            field=models.PositiveSmallIntegerField(blank=True, choices=[
                (1, 'С оценкой рисков возникновения коррупционных проявлений'),
                (2, 'С проверкой реализации приоритетных и национальных проектов'),
                (3, 'С проверкой соблюдения порядка управления и распоряжения имуществом'),
                (4, 'С проверкой порядка и условий предоставления межбюджетных трансфертов')], null=True),
        ),
    ]
