# Generated by Django 2.2.6 on 2019-10-28 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0008_kso_entity'),
    ]

    operations = [
        migrations.AddField(
            model_name='entity',
            name='founders',
            field=models.ManyToManyField(blank=True, db_index=True, related_name='_entity_founders_+', to='directory.Entity'),
        ),
    ]
