from django.db import models


class Employee(models.Model):
    """
    Работник КСО
    """

    # Ссылка на организацию
    organization_kso = models.ForeignKey(
        'OrganizationKso',
        on_delete=models.CASCADE,
        related_name='employees'
    )

    # Фамилия, имя, отчество
    name_last = models.CharField(max_length=20)
    name_first = models.CharField(max_length=20)
    name_second = models.CharField(max_length=20)

    # Должность, отдел
    department = models.CharField(max_length=30)
    position = models.CharField(max_length=30)

    # Телефон, эл. почта
    phone = models.CharField(max_length=30)
    email = models.CharField(max_length=30)

    def __str__(self):
        return '{} {} {}'.format(self.name_last, self.name_first, self.name_second)
