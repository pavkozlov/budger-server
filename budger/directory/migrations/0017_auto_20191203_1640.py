# Generated by Django 2.2.6 on 2019-12-03 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0016_entity_relevance_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ksoemployee',
            name='inactive_title',
            field=models.CharField(blank=True, db_index=True, default=None, max_length=2000, null=True),
        ),
    ]
