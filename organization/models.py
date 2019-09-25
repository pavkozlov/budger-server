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


class OrganizationKso(models.Model):
    """
    Организация - КСО
    """

    class Meta:
        ordering = ['title']

    # Ссылка на справочник ЕГРЮЛ
    organization_common = models.OneToOneField(
        'OrganizationCommon',
        on_delete=models.SET_NULL,
        related_name='organization_kso',
        null=True
    )

    # Название
    title = models.CharField(max_length=200)

    def __str__(self):
        return '{}'.format(self.title)


class OrganizationCommon(models.Model):
    """
    Справочник ЕГРЮЛ
    """

    class Meta:
        ordering = ['title_full']

    # Дата регистрации
    reg_date = models.DateField()

    # Наименование ОПФ
    opf_full = models.CharField(max_length=50)
    opf_short = models.CharField(max_length=5)

    # Наименование ЮЛ
    title_full = models.CharField(max_length=200)
    title_short = models.CharField(max_length=100)

    # ИНН, КПП, ОГРН
    inn = models.CharField(max_length=12)
    kpp = models.CharField(max_length=9)
    ogrn = models.CharField(max_length=13)

    # Адрес
    addr_index = models.CharField(max_length=6)
    addr_region = models.CharField(max_length=20)
    addr_locality = models.CharField(max_length=20)
    addr_street = models.CharField(max_length=20)
    addr_building = models.CharField(max_length=5)
    addr_housing = models.CharField(max_length=5)
    addr_office = models.CharField(max_length=5)

    # Руководитель
    head_position = models.CharField(max_length=20)
    head_name_last = models.CharField(max_length=20)
    head_name_first = models.CharField(max_length=20)
    head_name_second = models.CharField(max_length=20)
    head_accession_date = models.DateField()

    # Служебные
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - {}'.format(self.inn, self.title_full)
