# Generated by Django 2.2.8 on 2019-12-11 13:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0030_auto_20191211_1602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='responsible_department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='responded_events', to='directory.KsoDepartment1'),
        ),
        migrations.AlterField(
            model_name='event',
            name='responsible_employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='responded_events', to='directory.KsoEmployee'),
        ),
    ]
