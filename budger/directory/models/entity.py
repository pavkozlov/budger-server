from django.db import models
from django.contrib.postgres.fields import ArrayField


class Entity(models.Model):
    """
    Юридическое лицо | индивидуальный предприниматель.
    Данные импортируются из справочника ЕГРЮЛ.
    """

    # Дата регистрации
    reg_date = models.DateField()

    # Дата прекращения
    term_date = models.DateField(null=True, blank=True)

    # Наименование ОПФ
    opf_full = models.CharField(max_length=300, null=True, blank=True)
    opf_code = models.CharField(max_length=1000, null=True, blank=True)

    # Наименование ЮЛ
    title_full = models.CharField(max_length=1000)
    title_short = models.CharField(max_length=1000, null=True, blank=True)
    title_search = models.CharField(max_length=2001, default='', db_index=True)

    # ИНН, КПП, ОГРН
    inn = models.CharField(max_length=12, db_index=True)
    kpp = models.CharField(max_length=9, null=True, blank=True)
    ogrn = models.CharField(max_length=13)

    # Адрес
    addr_index = models.CharField(max_length=6, null=True, blank=True)
    addr_region_code = models.CharField(max_length=2)
    addr_region_type = models.CharField(max_length=1000)
    addr_region_title = models.CharField(max_length=1000)
    addr_locality_type = models.CharField(max_length=1000)
    addr_locality_title = models.CharField(max_length=1000)
    addr_street = models.CharField(max_length=1000, null=True, blank=True)
    addr_building = models.CharField(max_length=1000, null=True, blank=True)
    addr_housing = models.CharField(max_length=1000, null=True, blank=True)
    addr_office = models.CharField(max_length=1000, null=True, blank=True)

    # Руководитель
    head_position = models.CharField(max_length=300, null=True, blank=True)
    head_name_last = models.CharField(max_length=1000)
    head_name_first = models.CharField(max_length=1000)
    head_name_second = models.CharField(max_length=1000)
    head_accession_date = models.DateField(null=True, blank=True)

    # Служебные
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # Изменения ЮЛ
    updates = models.TextField(blank=True, null=True)

    # Учредители
    founders = ArrayField(models.CharField(max_length=12), blank=True, null=True)

    class Meta:
        ordering = ['title_full']

    def __str__(self):
        return '{} - {}'.format(self.inn, self.title_full)
