"""
Наполнение данными справочников:
- ЮЛ
- КСО
- Структурные подразделения КСО
- Сотрудники КСО
"""

import os
import json
import xml.dom.minidom
from django.db import migrations
from django.db.utils import IntegrityError
from budger.directory.import_data.fns_xml_parser import parse_elem
from budger.directory.import_data.kso_json_parser import transform
from budger.directory.import_data.kso_employees_json_parser import KsoEmployeeJsonParser


def populate_entities(apps, schema_editor):
    """ Наполнение данными справочника ЮЛ """

    Entity = apps.get_model('directory', 'Entity')
    Entity.objects.all().delete()

    xml_file_path = os.path.join(
        'budger',
        'directory',
        'import_data',
        'EGRUL_FULL_2019-01-01_385809.XML'
    )

    with open(xml_file_path, 'r', encoding='utf-8') as xml_file:
        doc = xml.dom.minidom.parse(xml_file)
        elements = doc.documentElement.getElementsByTagName('СвЮЛ')
        for elem in elements:
            model = parse_elem(elem)
            Entity.objects.create(**model)


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


def populate_kso_departments_and_employees(apps, schema_editor):
    """ Наполнение данными справочников структурных подразделений и работников КСО """

    Kso = apps.get_model('directory', 'Kso')
    KsoDepartment1 = apps.get_model('directory', 'KsoDepartment1')
    KsoDepartment2 = apps.get_model('directory', 'KsoDepartment2')
    KsoEmployee = apps.get_model('directory', 'KsoEmployee')

    KsoEmployee.objects.all().delete()
    KsoDepartment2.objects.all().delete()
    KsoDepartment1.objects.all().delete()

    parser = KsoEmployeeJsonParser(os.path.join(
        'budger',
        'directory',
        'import_data',
        'kso_employees.json'
    ))

    parsed_data = parser.exec()

    # Поле KSO можно менять сразу.
    # Делаем это в отдельном цикле чтобы читалось проще.
    for item in parsed_data:
        item['kso'] = Kso.objects.get(title_short=item['kso']['title_short'])

    # Сначала создаем departments1, так как нам понадобятся их ID,
    for item in parsed_data:
        if item.get('department1', None):
            KsoDepartment1.objects.get_or_create(
                kso=item['kso'],
                title=item['department1']
            )

    # Теперь создаем departments2, так как нам понадобятся и их ID
    for item in parsed_data:
        if item.get('department1', None) and item.get('department2', None):
            KsoDepartment2.objects.get_or_create(
                kso=item['kso'],
                department1=KsoDepartment1.objects.get(
                    kso=item['kso'],
                    title=item['department1']
                ),
                title=item['department2']
            )

    # Теперь, когда все ID на месте, можно создать сотрудников
    for item in parsed_data:
        item['department1'] = KsoDepartment1.objects.get(
            kso=item['kso'],
            title=item['department1']
        )
        if item['department2'] is not None:
            item['department2'] = KsoDepartment2.objects.get(
                kso=item['kso'],
                department1=item['department1'],
                title=item['department2']
            )
        KsoEmployee.objects.create(**item)


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_entities),
        migrations.RunPython(populate_kso),
        migrations.RunPython(populate_kso_departments_and_employees),
    ]
