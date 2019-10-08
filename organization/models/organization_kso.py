from django.db import models


class OrganizationKso(models.Model):
    """
    Организация - КСО
    """

    class Meta:
        ordering = ['title']

    # Ссылка на справочник ЕГРЮЛ
    organization = models.OneToOneField(
        'Organization',
        on_delete=models.SET_NULL,
        related_name='organization_kso',
        null=True
    )

    # Название
    title = models.CharField(max_length=200)

    def __str__(self):
        return '{}'.format(self.title)
