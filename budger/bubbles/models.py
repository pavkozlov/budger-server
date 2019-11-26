from django.db import models
from budger.directory.models.entity import Entity


class BudgetData(models.Model):
    """
    Модель для информации о планировании бюджета.
    Источник данных: http://budget.gov.ru/epbs/registry/SBRCOSTSUBMO/data?filterbudget.budgetcode=46000000
    """

    id = models.BigAutoField(primary_key=True, editable=False)

    # Отношение к объекту контроля
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)

    # Сумма
    amount = models.FloatField()

    # Год, даты утверждения, начала действия записи, окончания действия записи
    year = models.IntegerField()
    approved = models.DateField()
    started = models.DateField()
    ended = models.DateField()

    # Информация о кодах разделов\подразделов классификации расходов бюджетов
    rzpr_code = models.CharField(max_length=4, db_index=True)

    # Информация о видах расходов бюджета
    kvr_code = models.CharField(max_length=3, db_index=True)

    # Информация о кодах целевых статей расходов бюджета
    kcsr_code = models.CharField(max_length=10, db_index=True)


class BudgetTitle(models.Model):

    rzpr_code = models.CharField(
        max_length=4,
        default=None,
        db_index=True,
        null=True, blank=True,
        unique=True
    )

    kvr_code = models.CharField(
        max_length=3,
        default=None,
        db_index=True,
        null=True, blank=True,
        unique=True
    )

    kcsr_code = models.CharField(
        max_length=10,
        default=None,
        db_index=True,
        null=True, blank=True,
        unique=True
    )

    title = models.CharField(max_length=2000)
