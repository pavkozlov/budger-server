# Generated by Django 2.2.6 on 2019-11-28 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0014_ksoemployee_inactive_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ksoemployee',
            name='email',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='ksoemployee',
            name='phone_landline',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='ksoemployee',
            name='phone_mobile',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
