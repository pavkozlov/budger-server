# Generated by Django 2.2.6 on 2019-11-21 08:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0007_workflow'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='status',
        ),
    ]