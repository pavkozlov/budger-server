# Generated by Django 2.2.6 on 2019-12-06 11:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0022_auto_20191206_1413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='directory.KsoEmployee'),
        ),
    ]