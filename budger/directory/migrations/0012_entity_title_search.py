# Generated by Django 2.2.6 on 2019-10-28 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0011_auto_20191028_1616'),
    ]

    operations = [
        migrations.AddField(
            model_name='entity',
            name='title_search',
            field=models.CharField(default='', max_length=2001, db_index=True),
        ),
    ]
