from django.db import models


class Kso(models.Model):
    """
    Контрольно-счетная организация
    """

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

    class Meta:
        ordering = ['title_full']

    def __str__(self):
        return '{}'.format(self.title_short)


class KsoDepartment1(models.Model):
    """ Структурное подразделение КСО первого уровня """

    # Ссылка на организацию
    kso = models.ForeignKey(
        Kso,
        on_delete=models.CASCADE,
        related_name='departments'
    )

    # Наименование
    title = models.CharField(max_length=255)

    class Meta:
        ordering = ['title']
        unique_together = ('kso', 'title',)

    def __str__(self):
        return self.title


class KsoDepartment2(models.Model):
    """ Структурное подразделение КСО второго уровня """

    # Ссылка на организацию
    kso = models.ForeignKey(
        Kso,
        on_delete=models.CASCADE
    )

    department1 = models.ForeignKey(
        KsoDepartment1,
        on_delete=models.CASCADE,
        related_name='sub_departments'
    )

    # Название
    title = models.CharField(max_length=255)

    class Meta:
        ordering = ['title']
        unique_together = ('department1', 'title',)

    def __str__(self):
        return '{}'.format(self.title)


class KsoEmployee(models.Model):
    """
    Работник контрольно-счетной организации
    """

    # Ссылка на организацию
    kso = models.ForeignKey(
        'Kso',
        on_delete=models.CASCADE,
        related_name='employees'
    )

    department1 = models.ForeignKey(
        KsoDepartment1,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    department2 = models.ForeignKey(
        KsoDepartment2,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    # Фамилия, имя, отчество
    name = models.CharField(max_length=200)

    # Должность
    position = models.CharField(max_length=200)

    # Телефон, эл. почта
    phone_landline = models.CharField(max_length=200)
    phone_mobile = models.CharField(max_length=200)
    email = models.CharField(max_length=200)

    birth_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return '{} - {}'.format(self.name, self.kso)