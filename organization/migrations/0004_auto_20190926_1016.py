# Generated by Django 2.2.5 on 2019-09-26 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0003_auto_20190925_1941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organizationcommon',
            name='addr_housing',
            field=models.CharField(max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='organizationcommon',
            name='addr_office',
            field=models.CharField(max_length=5, null=True),
        ),
    ]