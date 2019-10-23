# Generated by Django 2.2.6 on 2019-10-22 12:23

from django.db import migrations
import os
import json


def populate_kso(apps, schema_editor):
    """ Наполнение данными справочника ЮЛ """
    Kso = apps.get_model('directory', 'Kso')

    json_file_path = os.path.join(
        'budger',
        'directory',
        'import_data',
        'kso_s_ogrn.json'
    )
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        s = json_file.read()
        d = json.loads(s)
        for kso in d:
            ogrn = kso.get('OGRN', None)
            title_full = kso.get('full_name', '')
            kso = Kso.objects.get(title_full=title_full)
            kso.ogrn = ogrn
            kso.save()


class Migration(migrations.Migration):
    dependencies = [
        ('directory', '0005_kso_ogrn'),
    ]

    operations = [
        migrations.RunPython(populate_kso),
    ]
