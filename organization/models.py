from django.db import models


class Employee(models.Model):
    """
    Работник КСО
    """
    organization_kso = models.ForeignKey(
        'OrganizationKso',
        on_delete=models.CASCADE,
        related_name='employees'
    )
    name = models.CharField(max_length=50)

    def __str__(self):
        return '{} - {}'.format(self.name, self.organization_kso)


class OrganizationKso(models.Model):
    """
    Организация - КСО
    """
    title = models.CharField(max_length=200)                # Название
    organization_common = models.OneToOneField(
        'OrganizationCommon',
        on_delete=models.SET_NULL,
        related_name='organization_kso',
        null=True
    )

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        ordering = ['title']


class OrganizationCommon(models.Model):
    """
    Организация из списка ЕГРЮЛ
    """
    title = models.CharField(max_length=200)    # Название
    ogrn = models.CharField(max_length=13)      # ОГРН
    inn = models.CharField(max_length=12)       # ИНН

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        ordering = ['title']


