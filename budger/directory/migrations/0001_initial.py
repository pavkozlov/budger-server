# Generated by Django 2.2.6 on 2019-10-17 09:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reg_date', models.DateField()),
                ('opf_full', models.CharField(max_length=100)),
                ('opf_code', models.CharField(max_length=10)),
                ('title_full', models.CharField(max_length=200)),
                ('title_short', models.CharField(max_length=200)),
                ('inn', models.CharField(max_length=12)),
                ('kpp', models.CharField(max_length=9)),
                ('ogrn', models.CharField(max_length=13)),
                ('addr_index', models.CharField(max_length=6)),
                ('addr_region_code', models.CharField(max_length=2)),
                ('addr_region_type', models.CharField(max_length=50)),
                ('addr_region_title', models.CharField(max_length=50)),
                ('addr_locality_type', models.CharField(max_length=50)),
                ('addr_locality_title', models.CharField(max_length=50)),
                ('addr_street', models.CharField(max_length=50)),
                ('addr_building', models.CharField(max_length=50)),
                ('addr_housing', models.CharField(max_length=50, null=True)),
                ('addr_office', models.CharField(max_length=50, null=True)),
                ('head_position', models.CharField(max_length=100)),
                ('head_name_last', models.CharField(max_length=30)),
                ('head_name_first', models.CharField(max_length=30)),
                ('head_name_second', models.CharField(max_length=30)),
                ('head_accession_date', models.DateField(null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['title_full'],
            },
        ),
        migrations.CreateModel(
            name='Kso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo', models.CharField(max_length=50)),
                ('title_full', models.CharField(max_length=200)),
                ('title_short', models.CharField(max_length=200)),
                ('chief_name', models.CharField(max_length=200)),
                ('addr_legal', models.CharField(max_length=200)),
                ('addr_fact', models.CharField(max_length=200)),
                ('www', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=100)),
                ('worker_count_staff', models.IntegerField()),
                ('worker_count_fact', models.IntegerField()),
                ('in_alliance', models.BooleanField()),
            ],
            options={
                'ordering': ['title_full'],
            },
        ),
        migrations.CreateModel(
            name='KsoDepartment1',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('kso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departments', to='directory.Kso')),
            ],
            options={
                'ordering': ['title'],
                'unique_together': {('kso', 'title')},
            },
        ),
        migrations.CreateModel(
            name='KsoDepartment2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('department1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_departments', to='directory.KsoDepartment1')),
                ('kso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='directory.Kso')),
            ],
            options={
                'ordering': ['title'],
                'unique_together': {('department1', 'title')},
            },
        ),
        migrations.CreateModel(
            name='KsoEmployee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('position', models.CharField(max_length=200)),
                ('phone_landline', models.CharField(max_length=200)),
                ('phone_mobile', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
                ('birth_date', models.DateField(null=True)),
                ('photo_slug', models.CharField(max_length=100, null=True)),
                ('department1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='directory.KsoDepartment1', null=True, blank=True)),
                ('department2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='directory.KsoDepartment2', null=True, blank=True)),
                ('kso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='directory.Kso')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
