from django.db import models
from budger.directory.models.entity import Entity
from .managers import AggregationManager


class BudgetAbstract(models.Model):
    """
    Абстрактная модель для работы с данными о планировании / исполении бюджета
    """
    id = models.BigAutoField(primary_key=True, editable=False)

    # Отношение к объекту контроля
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)

    # Сумма
    amount = models.FloatField()

    # Год
    year = models.IntegerField(db_index=True)

    # Информация о кодах разделов\подразделов классификации расходов бюджетов
    rzpr_code = models.CharField(max_length=4, db_index=True)

    # Информация о видах расходов бюджета
    kvr_code = models.CharField(max_length=3, db_index=True)

    # Информация о кодах целевых статей расходов бюджета
    kcsr_code = models.CharField(max_length=10, db_index=True)

    class Meta:
        abstract = True


class BudgetPlan(BudgetAbstract):
    """
    Модель для работы с данными запланированном бюджете.
    Источник данных:
    http://budget.gov.ru/epbs/registry/SBRCOSTSUBMO/data?filterbudget.budgetcode=46000000
    """

    # Даты утверждения, начала действия записи, окончания действия записи
    approved = models.DateField()
    started = models.DateField()
    ended = models.DateField()


class BudgetFact(BudgetAbstract):
    """
    Модель для работы с данными об исполнении бюджета.
    Источник данных:
    http://budget.gov.ru/epbs/registry/7710168360-CASHEXECEXPENSES/data?filterbudget.budgetcode=46000000
    """

    # Дата утверждения записи
    approved = models.DateField()  # appdatetime в источнике данных

    # Код и наименование цели
    goal_code = models.CharField(max_length=20, null=True, blank=True)
    goal_title = models.CharField(max_length=2000, null=True, blank=True)

    # Наименование полного кода расходов
    title = models.CharField(max_length=2000)


class BudgetTitle(models.Model):
    """
    Модель для работы с заголовками бюджетов:
    разделов\подразделов классификации расходов бюджетов,
    видах расходов бюджета
    кодах целевых статей расходов бюджета.
    """

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


class EntityBudget(models.Model):
    """
    Модель агрегированного бюджета (план и факт) для объекта контроля.
    """

    # Отношение к объекту контроля.
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)

    # Год.
    year = models.IntegerField(db_index=True)

    # Сумма плановая.
    amount_plan = models.FloatField(null=True, blank=True)

    # Сумма фактическая.
    amount_fact = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ('entity', 'year')


class Aggregation(models.Model):
    """
    Модель агрегированных параметров объекта контроля для РОП.
    """
    objects = AggregationManager()

    # Отношение к объекту контроля.
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)

    # Год даты актуальности данных.
    year = models.SmallIntegerField(db_index=True)

    # Сумма бюджета плановая.
    budget_amount_plan = models.FloatField(null=True, blank=True, db_index=True)

    # Сумма бюджета фактическая.
    budget_amount_fact = models.FloatField(null=True, blank=True, db_index=True)

    # Количество выявленных нарушений.
    violations_count = models.SmallIntegerField(null=True, blank=True, db_index=True)

    # Объем выявленных нарушений в руб.
    violations_amount = models.SmallIntegerField(null=True, blank=True, db_index=True)

    # Участие в рег. проекте.
    # Если ГРБС принимает участие в нескольких проектах, таблица содержит несколько записей.
    reg_project_participant = models.BooleanField(null=True, blank=True, db_index=True)

    # Размер бюджета в рег проекте
    reg_project_amount = models.BooleanField(null=True, blank=True, db_index=True)

    # Заметка о записи (any)
    memo = models.TextField(null=True, blank=True)
