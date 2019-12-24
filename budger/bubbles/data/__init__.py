from budger.bubbles.data.nat_projects import NAT_PROJECTS
from budger.bubbles.data.reg_projects import REG_PROJECTS
from collections import defaultdict
import re


def name_str_to_dict(s):
    m = re.search(r'([а-яА-Я-]+\s+[а-яА-Я]+\s+[а-яА-Я]+?)\s+-\s+(.+)', s)
    return {'name': m.group(1), 'position': m.group(2)} if m else s


class RegProject:
    queryset = REG_PROJECTS

    @staticmethod
    def get_amount_plan(proj):
        fed = ['межбюджетные трансферты в федеральный бюджет']
        mosobl = ['межбюджетные трансферты в бюджеты субъектов РФ', 'межбюджетные трансферты в БС',
                  'межбюджетные трансферты в МО других субъектов РФ',
                  'свод бюджетов Муниципальных образований, из них',
                  'бюджет субъекта, из них', 'межбюджетные трансферты в бюджеты МО']
        gos = ['межбюджетные трансферты в ТФОМС', 'межбюджетные трансферты из ГВБФ (справочно)',
               'межбюджетные трансферты в ГВБФ', 'ТФОМС']
        vne = ['определенные на федеральном уровне', 'привлеченные субъектом РФ']

        regproj_amount_plan_fed = 0.0
        regproj_amount_plan_local = 0.0
        regproj_amount_plan_gos = 0.0
        regproj_amount_plan_out = 0.0
        other = 0.0

        for res in proj:
            for finsupport in res['finsupports']:
                for year in range(2019, 2025):
                    if finsupport['finsource'] in fed:
                        regproj_amount_plan_fed += float(finsupport['fo{}'.format(year)])
                    elif finsupport['finsource'] in mosobl:
                        regproj_amount_plan_local += float(finsupport['fo{}'.format(year)])
                    elif finsupport['finsource'] in gos:
                        regproj_amount_plan_gos += float(finsupport['fo{}'.format(year)])
                    elif finsupport['finsource'] in vne:
                        regproj_amount_plan_out += float(finsupport['fo{}'.format(year)])
                    else:
                        other += float(finsupport['fo{}'.format(year)])

        return [{'title': 'Внебюджетные источники', 'sum': regproj_amount_plan_out},
                {'title': 'Бюджет московской области', 'sum': regproj_amount_plan_local},
                {'title': 'Бюджеты государственных внебюджетных фондов', 'sum': regproj_amount_plan_gos},
                {'title': 'Федеральный бюджет', 'sum': regproj_amount_plan_fed},
                {'title': '', 'sum': other, }]

    @staticmethod
    def transform(p):
        """
        Функция принимает региональный проект, трансформирует его в json заданного вида
        """

        def _aggregate_results(results):
            """
            Функция аггрегирует finsupports по годам
            """
            generated_results = []

            for item in results:
                result = {
                    'title': item['name'],
                    'end_date': item['result_end_date'],
                    'responsible': item['respexec'],
                    'fin': defaultdict(float)
                }
                for finsupport in item['finsupports']:
                    result['fin']['2019'] += float(finsupport['fo2019'])
                    result['fin']['2020'] += float(finsupport['fo2020'])
                    result['fin']['2021'] += float(finsupport['fo2021'])
                    result['fin']['2022'] += float(finsupport['fo2022'])
                    result['fin']['2023'] += float(finsupport['fo2023'])
                    result['fin']['2024'] += float(finsupport['fo2024'])
                generated_results.append(result)

            return generated_results

        def _aggregate_total(results):
            """
            Функция аггрегирует results по годам и по finsupports
            """
            result_total_fin = {
                'money': defaultdict(float),
            }

            for item in results:
                for finsupport in item['finsupports']:
                    result_total_fin['money']['2019'] += float(finsupport['fo2019'])
                    result_total_fin['money']['2020'] += float(finsupport['fo2020'])
                    result_total_fin['money']['2021'] += float(finsupport['fo2021'])
                    result_total_fin['money']['2022'] += float(finsupport['fo2022'])
                    result_total_fin['money']['2023'] += float(finsupport['fo2023'])
                    result_total_fin['money']['2024'] += float(finsupport['fo2024'])

                result_total_fin['fin'] = RegProject.get_amount_plan(results)
            return result_total_fin

        return {
            'title_full': p['title_full'],
            'title_short': p['title_short'],
            'grbs_title': p['grbs']['name'],
            'curator': name_str_to_dict(p['curator']),
            'responsible': name_str_to_dict(p['responsible']),
            'fpcode': p['fpcode'],
            'results': _aggregate_results(p['results']),
            'total': _aggregate_total(p['results'])
        }

    @staticmethod
    def get_by_id(id):
        for p in RegProject.queryset:
            if id == p['id']:
                return RegProject.transform(p)
        return None

    @staticmethod
    def get_by_grbs(grbs_id):
        projects = []
        for p in RegProject.queryset:
            if p['grbs']['grbs_id'] == grbs_id:
                projects.append(p)
        return projects

    @staticmethod
    def get_by_code(code):
        result = []
        for p in RegProject.queryset:
            if code in p['fpcode']:
                result.append({
                    'id': p['id'],
                    'code': p['fpcode'],
                    'title_short': p['fpname']
                })
        return result


class NatProject:
    @staticmethod
    def get_queryset():
        result = []
        for p in NAT_PROJECTS:
            if type(p['curator']) is str:
                p['curator'] = name_str_to_dict(p['curator'])
                p['curator']['position'] = ' '.join([p['curator']['position'], 'PФ'])
            if type(p['responsible']) is str:
                p['responsible'] = name_str_to_dict(p['responsible'])
                p['responsible']['position'] = ' '.join([p['responsible']['position'], 'PФ'])
            result.append(p)
        return result

    @staticmethod
    def list():
        result = []
        for p in NatProject.get_queryset():
            reg_projects = RegProject.get_by_code(p['code'])
            if reg_projects:
                result.append(
                    {
                        'id': p['id'],
                        'code': p['code'],
                        'title_short': p['title_short'],
                        'curator': p['curator'],
                        'responsible': p['responsible'],
                        'reg_projects': reg_projects,
                    }
                )
        return result
