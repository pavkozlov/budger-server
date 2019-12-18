from budger.bubbles.data.nat_projects import NAT_PROJECTS
from budger.bubbles.data.reg_projects import REG_PROJECTS
from collections import defaultdict
import re


def name_str_to_dict(s):
    m = re.search('(.+ .+ .+?) - (.+)', s)
    return {'name': m.group(1), 'position': m.group(2) + ' РФ'} if m else s


class RegProject:
    queryset = REG_PROJECTS

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
            fin_dict = defaultdict(float)

            for item in results:
                for finsupport in item['finsupports']:
                    result_total_fin['money']['2019'] += float(finsupport['fo2019'])
                    result_total_fin['money']['2020'] += float(finsupport['fo2020'])
                    result_total_fin['money']['2021'] += float(finsupport['fo2021'])
                    result_total_fin['money']['2022'] += float(finsupport['fo2022'])
                    result_total_fin['money']['2023'] += float(finsupport['fo2023'])
                    result_total_fin['money']['2024'] += float(finsupport['fo2024'])

                    fin_dict[finsupport['finsource']] += float(finsupport['fo2019'])
                    fin_dict[finsupport['finsource']] += float(finsupport['fo2020'])
                    fin_dict[finsupport['finsource']] += float(finsupport['fo2021'])
                    fin_dict[finsupport['finsource']] += float(finsupport['fo2022'])
                    fin_dict[finsupport['finsource']] += float(finsupport['fo2023'])
                    fin_dict[finsupport['finsource']] += float(finsupport['fo2024'])

                fin_list = zip(fin_dict.keys(), fin_dict.values())
                result_total_fin['fin'] = [{'title': i[0], 'sum': i[1]} for i in fin_list]
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
            if type(p['responsible']) is str:
                p['responsible'] = name_str_to_dict(p['responsible'])
            result.append(p)
        return result

    @staticmethod
    def list():
        result = []
        for p in NatProject.get_queryset():
            reg_projects = RegProject.get_by_code(p['code'])
            if reg_projects:

                curator = p['curator']
                if isinstance(name_str_to_dict(curator['name']), dict):
                    _curator = name_str_to_dict(curator['name'])
                    curator['name'] = _curator['name']
                    curator['position'] = ' - '.join([_curator['position'], curator['position']])

                result.append(
                    {
                        'id': p['id'],
                        'code': p['code'],
                        'title_short': p['title_short'],
                        'curator': curator,
                        'responsible': p['responsible'],
                        'reg_projects': reg_projects,
                    }
                )
        return result
