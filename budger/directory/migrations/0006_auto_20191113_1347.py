# Generated by Django 2.2.6 on 2019-11-13 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0005_merge_20191113_1346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entity',
            name='opf_code',
            field=models.CharField(blank=True, db_index=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='entity',
            name='org_status_code',
            field=models.CharField(choices=[('1', 'действующая'), ('2', 'недействующая'), ('3', 'отсутствуют правоотношения'), ('4', 'специальные указания')], db_index=True, max_length=1),
        ),
    ]