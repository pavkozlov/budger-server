from django.core.management.base import BaseCommand
import os
from budger.directory.models.kso import KsoEmployee, Kso
from django.contrib.auth.models import User


def read_csv(file):
    """
    Функция принимает имя файла, возвращает список из строк файла
    :param file: file name (str)
    :return: ['row1', 'row2', 'row3', ... ]
    """
    with open(file, 'r', encoding='utf-8') as f:
        data = f.readlines()
        data.pop(0)
        print('File {} has {} rows'.format(file, len(data)))
        return data


def parse_row(row):
    """
    Функция принимает строку, разделяет по ';', заменяет NULL -> None
    :param row:
    :return: list(param1, param2, param3, ...)
    """
    row_list = row.strip().split(';')
    if 'NULL' in row_list:
        for _ in range(row_list.count('NULL')):
            row_list[row_list.index('NULL')] = None
    return row_list


def get_user(user_id):
    """
    Функция принимает id User, возвращает User или None
    :param user_id:
    :return:
    """
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        user = None
    return user


def get_kso(kso_id):
    """
    Функция принимает id Kso, возвращает Kso или None
    :param kso_id:
    :return:
    """
    try:
        kso = Kso.objects.get(id=kso_id)
    except Kso.DoesNotExist:
        kso = None
    return kso


def update_ksoemployee(ksoemployee, row_list):
    """
    Функция принимает объект KsoEmployee и обновляет его параметры из списка row_list.
    :param ksoemployee:
    :param row_list:
    :return:
    """
    kso = get_kso(row_list[9])
    if kso is None:
        print('KsoEmployee with id {} have incorrect data (kso_id = {})'.format(row_list[0], row_list[9]))
        return

    if row_list[10] is not None:
        user = get_user(row_list[10])
        if user is None:
            print('KsoEmployee with id {} have incorrect data (user_id = {})'.format(row_list[0], row_list[10]))
            return
    else:
        user = None

    ksoemployee.id = row_list[0]
    ksoemployee.name = row_list[1]
    ksoemployee.position = row_list[2]
    ksoemployee.phone_landline = row_list[3]
    ksoemployee.phone_mobile = row_list[4]
    ksoemployee.email = row_list[5]
    ksoemployee.birth_date = row_list[6]
    ksoemployee.department1_id = row_list[7]
    ksoemployee.department2_id = row_list[8]
    ksoemployee.kso = kso
    ksoemployee.user = user
    ksoemployee.photo_slug = row_list[11]
    ksoemployee.is_head = row_list[12]
    ksoemployee.can_be_responsible = row_list[13]
    ksoemployee.save()
    return True


class Command(BaseCommand):
    help = 'A script for updating data in KSO employees from .csv file. The path to the file is specified into --f'

    def handle(self, *args, **options):
        if options['f']:
            path = os.path.join(os.getcwd(), options['f'][0])
        else:
            print('Provide path to csv file')
            exit(1)

        updated_counter = 0
        created_counter = 0
        data = read_csv(path)

        for row in data:
            row_list = parse_row(row)
            try:
                ksoepmloyee = KsoEmployee.objects.get(id=row_list[0])
                updated = update_ksoemployee(ksoepmloyee, row_list)

                if updated:
                    updated_counter += 1

            except KsoEmployee.DoesNotExist:

                kso = get_kso(row_list[9])
                if kso is None:
                    print('KsoEmployee with id {} have incorrect data (kso_id = {})'.format(row_list[0], row_list[9]))
                    continue

                user = get_user(row_list[10])
                if user is None:
                    print('KsoEmployee with id {} have incorrect data (user_id = {})'.format(row_list[0], row_list[10]))
                    continue

                KsoEmployee.objects.create(
                    id=row_list[0],
                    name=row_list[1],
                    position=row_list[2],
                    phone_landline=row_list[3],
                    phone_mobile=row_list[4],
                    email=row_list[5],
                    birth_date=row_list[6],
                    department1_id=row_list[7],
                    department2_id=row_list[8],
                    kso=kso,
                    user=user,
                    photo_slug=row_list[11],
                    is_head=row_list[12],
                    can_be_responsible=row_list[13],
                )
                created_counter += 1

        print('Successfully updated {} rows'.format(updated_counter))
        print('Created {} new rows'.format(created_counter))

    def add_arguments(self, parser):
        parser.add_argument('--f', action='append', type=str)
