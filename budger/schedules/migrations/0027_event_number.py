# Generated by Django 2.2.8 on 2019-12-10 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0026_auto_20191210_1803'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='number',
            field=models.SmallIntegerField(blank=True, db_index=True, null=True),
        ),
    ]
