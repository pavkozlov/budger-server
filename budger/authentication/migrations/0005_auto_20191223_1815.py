# Generated by Django 2.2.8 on 2019-12-23 15:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0025_auto_20191213_1412'),
        ('authentication', '0004_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='backlogentity',
            unique_together={('employee', 'entity')},
        ),
    ]
