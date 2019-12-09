from django.core.management.base import BaseCommand
from budger.directory.models.kso import KsoEmployee
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Script for creating users for KsoEmployees'

    def handle(self, *args, **options):
        employees = KsoEmployee.objects.filter(kso_id=1)

        for employee in employees:
            user = employee.user
            if user:
                print(user.username)
                user.set_password('admin')
                user.save()
