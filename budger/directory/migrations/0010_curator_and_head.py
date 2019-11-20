# Generated by Django 2.2.6 on 2019-11-20 12:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0009_municipalbudget'),
    ]

    operations = [
        migrations.AddField(
            model_name='ksodepartment1',
            name='curator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='curated_department', to='directory.KsoEmployee'),
        ),
        migrations.AddField(
            model_name='ksodepartment1',
            name='head',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='headed_department', to='directory.KsoEmployee'),
        ),
    ]
