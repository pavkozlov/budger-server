from django.core.management.base import BaseCommand
from budger.bubbles.data.reg_projects import REG_PROJECTS
from budger.directory.models.entity import Entity
from budger.bubbles.models import Aggregation
import os
from django.db import connection
import re
import string


def clean_database():
    with connection.cursor() as cursor:
        sql = """DELETE FROM bubbles_aggregation WHERE
                    violations_count IS NOT null 
                    OR regproj_participant IS NOT null"""
        cursor.execute(sql)


def get_amount_plan(res, year):
    fed = ['межбюджетные трансферты в федеральный бюджет']
    mosobl = ['межбюджетные трансферты в бюджеты субъектов РФ', 'межбюджетные трансферты в БС',
              'межбюджетные трансферты в МО других субъектов РФ',
              'свод бюджетов Муниципальных образований, из них',
              'бюджет субъекта, из них', 'межбюджетные трансферты в бюджеты МО']
    gos = ['межбюджетные трансферты в ТФОМС', 'ТФОМС', 'межбюджетные трансферты из ГВБФ (справочно)',
           'межбюджетные трансферты в ГВБФ']
    vne = ['определенные на федеральном уровне', 'привлеченные субъектом РФ']

    regproj_amount_plan_fed = 0.0
    regproj_amount_plan_local = 0.0
    regproj_amount_plan_gos = 0.0
    regproj_amount_plan_out = 0.0

    # parent
    fed_p = 0.0
    local_p = 0.0
    gos_p = 0.0
    out_p = 0.0

    for finsupport in res['finsupports']:

        if finsupport['finsource'] == 'межбюджетные трансферты из федерального бюджета (справочно)':
            fed_p += float(finsupport['fo{}'.format(year)])
        elif finsupport['finsource'] == 'консолидированный бюджет субъекта, из них':
            local_p += float(finsupport['fo{}'.format(year)])
        elif finsupport['finsource'] == 'внебюджетные источники,из них':
            out_p += float(finsupport['fo{}'.format(year)])
        elif finsupport['finsource'] == 'ТФОМС':
            gos_p += float(finsupport['fo{}'.format(year)])
        elif finsupport['finsource'] in fed:
            regproj_amount_plan_fed += float(finsupport['fo{}'.format(year)])
        elif finsupport['finsource'] in mosobl:
            regproj_amount_plan_local += float(finsupport['fo{}'.format(year)])
        elif finsupport['finsource'] in gos:
            regproj_amount_plan_gos += float(finsupport['fo{}'.format(year)])
        elif finsupport['finsource'] in vne:
            regproj_amount_plan_out += float(finsupport['fo{}'.format(year)])

    return {
        'regproj_amount_plan_out': regproj_amount_plan_out if out_p == 0 else out_p,
        'regproj_amount_plan_local': regproj_amount_plan_local if local_p == 0 else local_p,
        'regproj_amount_plan_gos': regproj_amount_plan_gos if gos_p == 0 else gos_p,
        'regproj_amount_plan_fed': regproj_amount_plan_fed if fed_p == 0 else fed_p
    }


def aggregation_from_json():
    for p in REG_PROJECTS:
        for res in p['results']:
            if type(res['GRBS']) is not dict:
                continue
            else:
                entity = Entity.objects.get(id=res['GRBS']['id'])
            memo = ' / '.join([p['title_full'].strip(), res['name'].strip(), res['result_end_date'].strip()])
            years = range(2019, 2025)

            for year in years:
                amount_plan = get_amount_plan(res, year)
                Aggregation.objects.create(
                    memo=memo,
                    entity=entity,
                    year=year,
                    regproj_participant=True,
                    regproj_amount_plan_fed=amount_plan['regproj_amount_plan_fed'],
                    regproj_amount_plan_local=amount_plan['regproj_amount_plan_local'],
                    regproj_amount_plan_gos=amount_plan['regproj_amount_plan_gos'],
                    regproj_amount_plan_out=amount_plan['regproj_amount_plan_out']
                )


def aggregation_from_csv(file_name):
    filename = os.path.join('budger', 'bubbles', 'data', file_name)
    with open(filename, 'r', encoding='UTF-8') as f:
        file = f.read().split('\n')
        file.pop(0)
        file.pop(-1)

    for line in file:
        l = line.split(';')

        if ',' in l[5]:
            violations_amount = l[5].split(',')[0]
        else:
            violations_amount = l[5]

        violations_count = l[4]

        year = l[1]
        memo = ' / '.join([l[0].strip(), l[3].strip()])
        entity_titles = l[2].split('|')

        for entity_title in entity_titles:
            title_search = re.sub(r'[{}«»]'.format(string.punctuation), ' ', entity_title)
            title_search = re.sub(r'\s+', ' ', title_search)
            title_search = title_search.strip(' ').upper()

            entity = Entity.objects.filter(title_search__contains=title_search)
            if entity.count() == 0:
                # print('!НЕ НАЙДЕНО: {}'.format(title_search))
                continue

            Aggregation.objects.create(
                violations_count=violations_count,
                violations_amount=violations_amount,
                memo=memo,
                entity=entity.first(),
                year=year,
                regproj_participant=False
            )


class Command(BaseCommand):
    help = 'Script for inserting aggregation into db'

    def handle(self, *args, **options):
        clean_database()
        aggregation_from_json()
        aggregation_from_csv('2017-2019plan.csv')
        aggregation_from_csv('2017-2019Нарушения.csv')
