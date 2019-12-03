# Generated by Django 2.2.6 on 2019-11-29 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('code', models.CharField(db_index=True, max_length=300)),
                ('uuid', models.CharField(max_length=300, unique=True)),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'success'), (2, 'warning'), (3, 'error')])),
                ('created', models.DateField()),
                ('description', models.CharField(blank=True, max_length=2000, null=True)),
            ],
            options={
                'db_table': 'jobs_log',
                'ordering': ['-created'],
                'permissions': [('dashboard.can_view_jobs', 'Can view jobs list.')],
            },
        ),
    ]