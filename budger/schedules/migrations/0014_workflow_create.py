# Generated by Django 2.2.6 on 2019-11-27 06:47


import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('schedules', '0013_refactor_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='status',
            field=models.PositiveSmallIntegerField(
                blank=True,
                choices=[(10, 'Черновик'), (20, 'В работе'), (30, 'Согласовано')],
                db_index=True, default=10, null=True),
        ),
        migrations.AlterField(
            model_name='workflow',
            name='memo',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='workflow',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Согласовано'), (1, 'Не согласовано')]),
        ),
        migrations.AlterField(
            model_name='event',
            name='subject',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.PositiveSmallIntegerField(
                choices=[(1, 'Финансовый аудит (контроль)'), (2, 'Аудит в сфере закупок'), (3, 'Аудит эффективности'),
                         (4, 'Экспертиза проекта закона'), (5, 'Финансово-экономическая экспертиза')]), blank=True,
                                                            default=None, null=True, size=None),
        ),
    ]
