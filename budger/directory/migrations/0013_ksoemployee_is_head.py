# Generated by Django 2.2.6 on 2019-10-29 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0012_entity_title_search'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kso',
            name='chief_name',
        ),
        migrations.AddField(
            model_name='ksoemployee',
            name='is_head',
            field=models.BooleanField(default=False, db_index=True),
        ),
    ]
