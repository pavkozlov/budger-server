# Generated by Django 2.2.6 on 2019-11-14 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0006_auto_20191113_1347'),
    ]

    operations = [
        migrations.AddField(
            model_name='entity',
            name='oktmo_code',
            field=models.CharField(blank=True, max_length=11, null=True),
        ),
        migrations.AddField(
            model_name='entity',
            name='oktmo_title',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
