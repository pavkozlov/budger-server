# Generated by Django 2.2.5 on 2019-09-05 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0003_record_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='amount',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='record',
            name='description',
            field=models.TextField(null=True),
        ),
    ]
