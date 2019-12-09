from django.core.management.base import BaseCommand
from budger.directory.models.kso import KsoEmployee
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Script for creating users for KsoEmployees'

    def handle(self, *args, **options):
        employees = KsoEmployee.objects.filter(kso_id=1)

        for employee in employees:
            if employee.email is None or len(employee.email) < 1:
                continue

            u_data = {
                'username': employee.email.split('@')[0].lower(),
                'email': employee.email.lower(),
                'password': 'admin'
            }

            u = User.objects.filter(username=u_data['username'], email=u_data['email'])

            user = User.objects.create_user(u_data) if not u.exists else u.first()

            employee.user = user
            employee.save()
