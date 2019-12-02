from rest_framework_csv.renderers import CSVRenderer


class KsoCsvRenderer (CSVRenderer):
    header = [
        'id',
        'title_short',
        'www',
        'email',
        'phone',
        'addr_fact',
        'employees_count_staff',
        'in_alliance'
    ]