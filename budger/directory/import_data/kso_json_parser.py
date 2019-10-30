
def transform(obj: dict):
    """ Трансформация данных из json в dict, пригодный для построения модели OrganizationKso """

    def get_bool(key: str):
        s = obj.get(key, '')
        return True if s == '1' else False

    def get_int(key: str):
        s = obj.get(key, '0')
        try:
            return int(s)
        except ValueError:
            return 0

    return {
        'logo': obj.get('logo', ''),
        'title_full': obj.get('full_name', ''),
        'title_short': obj.get('short_name', ''),
        'chief_name': obj.get('head', ''),
        'addr_legal': obj.get('adress', ''),
        'addr_fact': obj.get('adress_fact', ''),
        'www': obj.get('web', ''),
        'email': obj.get('mail', ''),
        'phone': obj.get('phone', ''),
        'worker_count_staff': get_int('worker_count'),
        'worker_count_fact': get_int('worker_count_fact'),
        'in_alliance': get_bool('union')
    }
