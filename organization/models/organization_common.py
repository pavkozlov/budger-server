from django.db import models


class OrganizationCommon(models.Model):
    """
    Справочник ЕГРЮЛ
    """

    class Meta:
        ordering = ['title_full']

    # Дата регистрации
    reg_date = models.DateField()

    # Наименование ОПФ
    opf_full = models.CharField(max_length=100)
    opf_code = models.CharField(max_length=10)

    # Наименование ЮЛ
    title_full = models.CharField(max_length=200)
    title_short = models.CharField(max_length=200)

    # ИНН, КПП, ОГРН
    inn = models.CharField(max_length=12)
    kpp = models.CharField(max_length=9)
    ogrn = models.CharField(max_length=13)

    # Адрес
    addr_index = models.CharField(max_length=6)
    addr_region_code = models.CharField(max_length=2)
    addr_region_type = models.CharField(max_length=50)
    addr_region_title = models.CharField(max_length=50)
    addr_locality_type = models.CharField(max_length=50)
    addr_locality_title = models.CharField(max_length=50)
    addr_street = models.CharField(max_length=50)
    addr_building = models.CharField(max_length=50)
    addr_housing = models.CharField(max_length=50, null=True)
    addr_office = models.CharField(max_length=50, null=True)

    # Руководитель
    head_position = models.CharField(max_length=100)
    head_name_last = models.CharField(max_length=30)
    head_name_first = models.CharField(max_length=30)
    head_name_second = models.CharField(max_length=30)
    head_accession_date = models.DateField(null=True)

    # Служебные
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - {}'.format(self.inn, self.title_full)
