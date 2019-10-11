from django.db import models


class Kso(models.Model):
    """
    Контрольно-счетная организация
    """

    class Meta:
        ordering = ['title_full']

    # Наименование изображения с логотипом
    logo = models.CharField(max_length=50)

    # Название
    title_full = models.CharField(max_length=200)
    title_short = models.CharField(max_length=200)

    # Руководитель
    chief_name = models.CharField(max_length=200)

    # Адреса и контакты
    addr_legal = models.CharField(max_length=200)
    addr_fact = models.CharField(max_length=200)
    www = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)

    # Численность сотрудников
    worker_counts_staff = models.IntegerField()
    worker_count_fact = models.IntegerField()

    # Состоит в СМ КСО
    in_alliance = models.BooleanField()

    def __str__(self):
        return '{}'.format(self.title_short)


class KsoEmployee(models.Model):
    """
    Работник контрольно-счетной организации
    """

    class Meta:
        ordering = ['name']

    # Ссылка на организацию
    kso = models.ForeignKey(
        'Kso',
        on_delete=models.CASCADE,
        related_name='employees'
    )

    # Фамилия, имя, отчество
    name = models.CharField(max_length=200)

    # Должность, отдел
    department = models.CharField(max_length=200)
    position = models.CharField(max_length=200)

    # Телефон, эл. почта
    phone_landline = models.CharField(max_length=200)
    phone_mobile = models.CharField(max_length=200)
    email = models.CharField(max_length=200)

    birth_date = models.DateField(null=True)

    def __str__(self):
        return '{} - {}'.format(self.name, self.kso)
