import json
import os
from datetime import date
from .json_parser import x_departments


class KsoEmployeeJsonParser:
    def __init__(self, json_file_path):
        # Load data
        json_file = open(json_file_path, 'r', encoding='utf-8')
        self.data = json.loads(json_file.read())

        # Load and prepare KSO lookup
        self.kso_lookup = self._load_kso_lookup()

    @staticmethod
    def _load_kso_lookup():
        kso_lookup = {}

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
                kso_lookup[str(kso['id'])] = kso['short_name']

        return kso_lookup

    def exec(self):
        result = []
        for obj in self.data:
            item = self.transform(obj)
            if item:
                result.append(self.transform(obj))
        return result

    def transform(self, obj: dict):
        """ Трансформация данных из json в dict, пригодный для построения модели KsoEmployee """

        def get_date(key: str):
            s = obj.get(key, None)

            if s is not None and len(s) == 10:
                d, m, y = s.split('.')
                return date(int(y), int(m), int(d))

            return None

        # Find out kso
        kso = {
            'title_short': self.kso_lookup[obj['ID_kso']]
        }

        department1, department2 = x_departments(obj)

        if obj.get('name', '').strip() != '':
            return {
                'kso': kso,
                'name': obj.get('name', ''),
                'department1': department1 or kso['title_short'],
                'department2': department2,
                'position': obj.get('position', ''),
                'phone_landline': obj.get('work_phone', ''),
                'phone_mobile': obj.get('mob_phone', ''),
                'email': obj.get('email', ''),
                'birth_date': get_date('birth_date'),
                'photo_slug': obj.get('photo', ''),
            }

        return None
