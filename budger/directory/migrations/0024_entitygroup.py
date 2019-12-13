# Generated by Django 2.2.8 on 2019-12-13 08:52

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0023_municipalbudget_administration'),
    ]

    operations = [
        migrations.CreateModel(
            name='EntityGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(db_index=True, max_length=100, unique=True)),
                ('data', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None)),
            ],
        ),
    ]
