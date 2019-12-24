from django.core.management.base import BaseCommand
from budger.bubbles.data.reg_projects import REG_PROJECTS
from budger.directory.models.entity import Entity
import json
import os


class Command(BaseCommand):
    help = 'Script for updating json'

    def handle(self, *args, **options):
        not_found = []

        queryset = REG_PROJECTS
        for p in queryset:
            for res in p['results']:
                grbs_inn = res['GRBS']
                entity_qs = Entity.objects.filter(inn=grbs_inn)

                if entity_qs.count() == 1:
                    entity = entity_qs.first()
                elif entity_qs.count() > 1:
                    entity = None
                    for e in entity_qs:
                        t1 = e.kbk_title.upper()
                        t2 = t1 + ' МОСКОВСКОЙ ОБЛАСТИ'
                        if e.title_full in [t1, t2]:
                            entity = e
                elif not entity_qs.exists():
                    entity = None

                if entity is not None:
                    res['GRBS'] = {
                        'id': entity.id,
                        'title': entity.title_full,
                    }
                else:
                    not_found.append(grbs_inn)

        filepath = os.path.join('budger', 'bubbles', 'data', 'result.json')
        with open(filepath, 'w', encoding='utf8') as f:
            j = json.dumps(queryset, ensure_ascii=False).replace('\\"', " ' ")
            f.write(j)

        print(not_found)
