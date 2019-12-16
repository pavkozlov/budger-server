from django.core.management.base import BaseCommand
from budger.directory.models.kso import KsoEmployee
from django.contrib.auth.models import User
import random
import string

STAFF = ['KorolihinVV@mosreg.ru', 'admin@admin.ru']


def generate_password(password_len=8):
    chars = string.digits + string.ascii_letters
    password_list = random.choices(chars, k=password_len)
    return ''.join(password_list)


class Command(BaseCommand):
    help = 'Script for creating users for KsoEmployees or change password if user exists'

    def handle(self, *args, **options):
        employees = KsoEmployee.objects.filter(kso_id=1)

        for employee in employees:

            if employee.email in [None, '', *STAFF] or '@' not in employee.email:
                continue

            email = employee.email.lower()
            username = email.split('@')[0]
            password = generate_password()

            if employee.user is None:
                user = User.objects.create_user(username=username, email=email, password=password)
                employee.user = user
                employee.save()
            else:
                employee.user.set_password(password)
                employee.user.save()

            print('{} {}'.format(email, password))
