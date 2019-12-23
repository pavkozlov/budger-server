# Generated by Django 2.2.8 on 2019-12-23 08:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('directory', '0025_auto_20191213_1412'),
    ]

    operations = [
        migrations.CreateModel(
            name='BacklogEntity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('memo', models.TextField(blank=True, null=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='directory.KsoEmployee')),
                ('entity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='directory.Entity')),
            ],
        ),
    ]