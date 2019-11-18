from django.core.management.base import BaseCommand
import os
from . import _update_from_csv as update_from_csv
from . import _db_connections as db_connections


class Command(BaseCommand):
    help = 'Скрипт для обновления данных о работниках КСО из .csv файла. Путь к файлу указывается через --filepath'

    def handle(self, *args, **options):
        if options['filepath']:
            path = os.path.join(os.getcwd(), options['filepath'][0])
        else:
            print('Provide path to csv file')
            exit(1)

        counter = 0
        conn_jobs, conn_dj = db_connections.get()
        cur = conn_dj.cursor()
        data = update_from_csv.read_csv(path)

        for row in data:
            row_list = update_from_csv.parse_row(row)
            kso_employee_id = update_from_csv.update(cur, row_list)
            if kso_employee_id is not None:
                counter += 1

        conn_dj.commit()
        cur.close()
        conn_dj.close()
        print('Successfully updated {} rows'.format(counter))

    def add_arguments(self, parser):
        parser.add_argument('--filepath', action='append', type=str)
