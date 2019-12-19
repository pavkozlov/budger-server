from django.db import models
from budger.directory.models.entity import Entity, EntityGroup


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

    # Отношение к объекту контроля
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)

    # Год
    year = models.IntegerField(db_index=True)

    # Сумма плановая
    amount_plan = models.FloatField(null=True, blank=True)

    # Сумма фактическая
    amount_fact = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ('entity', 'year')


class EntityBubbleManager(models.Manager):
    OGRN = [
        ["1025002870837", "1027739562256"],
        ["1105001005340", "1075024000248", "1067746507344", "1035009553259", "1035000704749", "1035005501431",
         "1035005000117", "1057748113961", "1045022400070", "1115024000552", "1035008250474"],
        ["1025005245055", "1185053043174", "1125012008021", "1025002042009", "1125024004918", "1035004463230",
         "1125024004467"],
        ["1125024004973", "1135024006776", "1185053037476", "1095024003910", "1125024005920", "1027700546510",
         "1137799018081", "1045003352261", "1037739442707"],
        ["1027739119121", "1035009552654", "1025002870837", "1145040006517", "1025001766096", "1135024007887",
         "1125047013772", "1115024008868", "1037739557020"],
        ["1027700524037", "1027739809460", "1125024004709", "1035000700668", "1037700160222", "1037719012407",
         "1125047008569", "1135024006831", "1165024054161", "1195053001747", "1125024000287"]
    ]

    INSPECTION_1 = 282
    INSPECTION_2 = 283
    INSPECTION_3 = 284
    INSPECTION_4 = 285
    INSPECTION_5 = 286
    INSPECTION_6 = 287

    def get_entities_by_inspection(self, department_id):

        def _get_id_list(ogrn_list):
            return list(Entity.objects.filter(ogrn__in=ogrn_list).values_list('id', flat=True))

        entities_id = None

        if department_id == self.INSPECTION_1:
            entities_id = _get_id_list(self.OGRN[0])
        elif department_id == self.INSPECTION_2:
            entities_id = _get_id_list(self.OGRN[1])
        elif department_id == self.INSPECTION_3:
            entities_id = _get_id_list(self.OGRN[2])
        elif department_id == self.INSPECTION_4:
            entities_id = _get_id_list(self.OGRN[3])
        elif department_id == self.INSPECTION_5:
            entities_id = _get_id_list(self.OGRN[4])
            entities_id += EntityGroup.objects.get(code='municipals').data
        elif department_id == self.INSPECTION_6:
            entities_id = _get_id_list(self.OGRN[5])

        if entities_id is not None:
            return super(EntityBubbleManager, self).get_queryset().filter(entity_id__in=entities_id)

        return super(EntityBubbleManager, self).none()


class EntityBubble(models.Model):
    """
    Модель агрегированных параметров объекта контроля для РОП.
    """

    # Отношение к объекту контроля
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)

    # Дата актуальности данных
    date = models.DateField(db_index=True)

    # Сумма бюджета плановая
    budget_amount_plan = models.FloatField(null=True, blank=True)

    # Сумма бюджета фактическая
    amount_fact = models.FloatField(null=True, blank=True)

    objects = EntityBubbleManager()
