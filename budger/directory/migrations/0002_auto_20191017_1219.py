"""
Наполнение данными справочников:
- ЮЛ
- КСО
- Структурные подразделения КСО
- Сотрудники КСО
"""

import os
import json
from django.db import migrations
from budger.directory.import_data.kso_json_parser import transform


def populate_kso(apps, schema_editor):
    """ Наполнение данными справочника КСО """

    Kso = apps.get_model('directory', 'Kso')
    Kso.objects.all().delete()

    json_file_path = os.path.join(
        'budger',
        'directory',
        'import_data',
        'kso.json'
    )

    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        s = json_file.read()
        d = json.loads(s)
        for kso in d:
            model = transform(kso)
            Kso.objects.create(**model)


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_kso),
    ]
