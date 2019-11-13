# Generated by Django 2.2.6 on 2019-11-11 09:45

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EntitySubordinates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tree', django.contrib.postgres.fields.jsonb.JSONField()),
            ],
        ),
        migrations.RemoveField(
            model_name='entity',
            name='addr_region_code',
        ),
        migrations.RemoveField(
            model_name='entity',
            name='opf_full',
        ),
        migrations.AddField(
            model_name='entity',
            name='kbk_code',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='entity',
            name='kbk_title',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='entity',
            name='ofk_code',
            field=models.CharField(db_index=True, default='', max_length=8),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='entity',
            name='ofk_regnum',
            field=models.CharField(db_index=True, default='', max_length=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='entity',
            name='okfs_code',
            field=models.CharField(default='', max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='entity',
            name='okfs_title',
            field=models.CharField(default='', max_length=250),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='entity',
            name='opf_title',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='entity',
            name='org_status_code',
            field=models.CharField(choices=[('1', 'действующая'), ('2', 'недействующая'), ('3', 'отсутствуют правоотношения'), ('4', 'специальные указания')], default='', max_length=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='entity',
            name='org_type_code',
            field=models.CharField(choices=[('02', 'орган управления государственным внебюджетным фондом'), ('03', 'учреждение'), ('05', 'унитарное предприятие'), ('09', 'государственная корпорация, государственная компания'), ('20', 'иные юридические лица, иные неучастники бюджетного процесса'), ('22', 'Центральный банк Российской Федерации (Банк России)')], default='', max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='entity',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='directory.Entity'),
        ),
        migrations.AlterField(
            model_name='entity',
            name='addr_building',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='entity',
            name='addr_housing',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='entity',
            name='addr_locality_title',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='entity',
            name='addr_locality_type',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='entity',
            name='addr_office',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='entity',
            name='addr_region_title',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='entity',
            name='addr_region_type',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='entity',
            name='addr_street',
            field=models.CharField(blank=True, max_length=1011, null=True),
        ),
        migrations.AlterField(
            model_name='entity',
            name='inn',
            field=models.CharField(blank=True, db_index=True, max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='entity',
            name='ogrn',
            field=models.CharField(blank=True, max_length=13, null=True),
        ),
        migrations.AlterField(
            model_name='entity',
            name='opf_code',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='entity',
            name='reg_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='entity',
            name='title_full',
            field=models.CharField(db_index=True, max_length=2000),
        ),
        migrations.AlterField(
            model_name='entity',
            name='title_search',
            field=models.CharField(db_index=True, default='', max_length=4001),
        ),
        migrations.AlterField(
            model_name='entity',
            name='title_short',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
        migrations.DeleteModel(
            name='FoundersTree',
        ),
        migrations.AddField(
            model_name='entitysubordinates',
            name='entity',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='directory.Entity'),
        ),
    ]