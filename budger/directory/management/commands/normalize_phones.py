from django.core.management.base import BaseCommand
from budger.directory.models.kso import KsoEmployee
import re


def normalize_phone_number(phone):
    """
    Функция принимает телефон в произвольном формате, возвращает только цифры
    :param phone:
    :return: str
    """
    if len(phone) == 0:
        return phone

    code = re.findall('\((\d*)\)', phone)
    country_code = code[0] if len(code) > 0 else None

    digits = re.findall('\d', phone)
    phone_number = ''.join([digit for digit in digits])

    if len(phone_number) == 10:
        phone_number = '8' + phone_number

    if country_code and phone_number.startswith(country_code):
        phone_number = '8' + phone_number

    if phone_number[0] != '8':
        phone_number = '8' + phone_number

    return phone_number


class Command(BaseCommand):
    help = 'Script for format phones in KspEmployees'

    def handle(self, *args, **options):
        employees = KsoEmployee.objects.all()

        for employee in employees:
            employee.phone_landline = normalize_phone_number(employee.phone_landline)
            employee.phone_mobile = normalize_phone_number(employee.phone_mobile)

            employee.save()
