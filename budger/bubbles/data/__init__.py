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
    queryset = NAT_PROJECTS

    @staticmethod
    def list():
        result = []
        for p in NatProject.queryset:
            reg_projects = RegProject.get_by_code(p['code'])
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
