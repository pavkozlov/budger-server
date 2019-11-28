from django.core.management.base import BaseCommand
from budger.directory.models.kso import KsoEmployee
import re


def clean_phone_number(phone):
    """
    Функция принимает телефон в произвольном формате, возвращает только цифры
    :param phone:
    :return: str
    """
    if phone is None:
        return None

    digits = re.findall('\d', phone)
    phone_number = ''.join([digit for digit in digits])

    return check_country_code(phone_number)


def check_country_code(number):
    """
    Функция принимает очищенный номер телефона, добавляет в начало 8, если её нет
    :param number:
    :return:
    """
    if len(number) == 10:
        return '8' + number
    else:
        return number


class Command(BaseCommand):
    help = 'Script for format phones in KspEmployees'

    def handle(self, *args, **options):
        employees = KsoEmployee.objects.all()

        for employee in employees:

            employee.phone_landline = clean_phone_number(employee.phone_landline)
            employee.phone_mobile = clean_phone_number(employee.phone_mobile)

            employee.save()
