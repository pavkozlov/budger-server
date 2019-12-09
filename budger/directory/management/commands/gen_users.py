from django.core.management.base import BaseCommand
from budger.directory.models.kso import KsoEmployee
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Script for creating users for KsoEmployees'

    def handle(self, *args, **options):
        employees = KsoEmployee.objects.filter(kso_id=1)

        for employee in employees:
            if employee.email not in [None, ''] and '@' in employee.email:
                print('{} ... '.format(employee.name), end='')

                data = {
                    'username': employee.email.split('@')[0].lower(),
                    'email': employee.email.lower(),
                    'password': 'admin'
                }

                try:
                    user = User.objects.get(email=data['email'])
                    print(user, 'applied.')
                except User.DoesNotExist:
                    user = User.objects.create_user(data)
                    print('created.')

                employee.user = user
                employee.save()


