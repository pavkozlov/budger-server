# Generated by Django 2.2.6 on 2019-12-06 09:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0020_auto_20191205_1832'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='workflow',
            options={'ordering': ['created'], 'permissions': [('manage_workflow', 'Управление согласованиями.')]},
        ),
    ]