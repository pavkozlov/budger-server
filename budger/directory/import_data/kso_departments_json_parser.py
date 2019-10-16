import json
import os
from datetime import date


class KsoDepartmentsJsonParser:
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
        """ Трансформация данных из json в dict, пригодный для построения модели KsoDepartment """

        # Find out kso
        kso = {
            'title_short': self.kso_lookup[obj['ID_kso']]
        }

        if obj.get('otdel', '').strip() != '':
            return {
                'kso': kso,
                'title': obj.get('otdel', ''),
            }

        return None
