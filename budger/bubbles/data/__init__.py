import re
from budger.bubbles.data.nat_projects import NAT_PROJECTS
from budger.bubbles.data.reg_projects import REG_PROJECTS


class RegProject:
    queryset = REG_PROJECTS

    @staticmethod
    def get_by_id(id):
        for p in RegProject.queryset:
            if id == p['id']:
                return p
        return None

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
        def _t(s):
            print('asd', s)
            if s:
                m = re.search('(.+ .+ .+?) - (.+)', s)
                if m:
                    return {'name': m.group(1), 'position': m.group(2)}
            return s

        result = []
        for p in NAT_PROJECTS:
            if type(p['curator']) is str:
                p['curator'] = _t(p['curator'])
            if type(p['responsible']) is str:
                p['responsible'] = _t(p['responsible'])
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
