# Generated by Django 2.2.6 on 2019-11-11 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='appeal_author',
            field=models.CharField(blank=True, db_index=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='appeal_date',
            field=models.DateField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='appeal_number',
            field=models.CharField(blank=True, db_index=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='attendant_kso',
            field=models.ManyToManyField(blank=True, db_index=True, to='directory.Kso'),
        ),
        migrations.AlterField(
            model_name='event',
            name='method',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Обследование'), (2, 'Проверка')], db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='mode',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Совместное'), (2, 'Самостоятельное'), (3, 'Параллельное')], db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='status',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'В работе'), (2, 'На согласовании'), (3, 'Согласовано')], db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='working_time',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]
