from django.db import models
from budger.directory.models.entity import Entity
from budger.directory.models.kso import Kso, KsoDepartment1, KsoEmployee
from django.contrib.postgres.fields import ArrayField

ANNUAL_STATUS_ENUM = [
    (1, 'В работе'),
    (2, 'На согласовании'),
    (3, 'Согласовано'),
]

EVENT_TYPE_ENUM = [
    (1, 'Контрольное'),
    (3, 'Экспертно-аналитическое'),
    (2, 'Экспертное'),
]

EVENT_SUBJECT_ENUM = [
    (1, 'Финансовый аудит (контроль)'),
    (3, 'Аудит в сфере закупок'),
    (2, 'Аудит эффективности'),
    (3, 'Экспертиза проекта закона'),
    (4, 'Финансово-экономическая экспертиза')
]

EVENT_MODE_ENUM = [
    (2, 'Самостоятельное мероприятие'),
    (1, 'Совместное мероприятие'),
    (3, 'Параллельное мероприятие'),
]

WORKFLOW_STATUS_ENUM = [
    (0, 'Черновик'),
    (1, 'Согласовано начальником инспекции'),
    (2, 'Согласовано аудитором'),
    (3, 'Согласовано Председателем'),
]

EVENT_INITIATOR_ENUM = [
    (0, 'По предложениям Губернатора Московской области / Главы муниципального образования'),
    (1, 'По поручениям Московской областной думы / Законодательного органа муниципального образования'),
    (2, 'По обращениям граждан'),
    (3, 'По обращениям общественных организаций'),
    (4, 'По обращениям правоохранительных органов'),
    (5, 'По решению Совета КСО МО'),
    (6, 'По решению органа аудита (контроля)'),
    (7, 'По обращениям Правительства Московской области / Администрации муниципального образования'),
]

EVENT_SUBTYPE_ENUM = [
    (0, 'С оценкой рисков возникновения коррупционных проявлений'),
    (1, 'С проверкой реализации приоритетных и национальных проектов'),
    (2, 'С проверкой соблюдения порядка управления и распоряжения имуществом'),
    (3, 'С проверкой порядка и условий предоставления межбюджетных трансфертов'),
]

EVENT_WAY_ENUM = [
    (0, 'С выездом'),
    (1, 'Камерально')
]


class Annual(models.Model):
    year = models.PositiveSmallIntegerField(db_index=True)
    status = models.PositiveSmallIntegerField(db_index=True, choices=ANNUAL_STATUS_ENUM)

    def __str__(self):
        return '{} - {}'.format(self.year, self.status)

    class Meta:
        ordering = ['-year']


class Event(models.Model):
    # Тип контроля
    type = models.PositiveSmallIntegerField(db_index=True, choices=EVENT_TYPE_ENUM, blank=True, null=True)

    # Тип мероприятия
    subject = ArrayField(models.PositiveSmallIntegerField(choices=EVENT_SUBJECT_ENUM), size=3, null=True, blank=True, default=None)

    # Наименование мероприятия
    title = models.CharField(max_length=255)

    # Основания для проведения мероприятия
    initiator = models.PositiveSmallIntegerField(choices=EVENT_INITIATOR_ENUM, null=True, blank=True)

    # Дополнительные признаки
    subtype = ArrayField(models.PositiveSmallIntegerField(choices=EVENT_SUBTYPE_ENUM), size=4, blank=True, null=True)

    # Проверяемый период
    period_from = models.DateField(db_index=True, null=True, blank=True)
    period_to = models.DateField(db_index=True, null=True, blank=True)

    # Метод проведения
    method = models.CharField(max_length=250, null=True, blank=True, db_index=True)

    # Способ проведения
    way = models.PositiveSmallIntegerField(db_index=True, choices=EVENT_WAY_ENUM, null=True, blank=True)

    # Даты проведения мероприятия
    exec_from = models.DateField(db_index=True)
    exec_to = models.DateField(db_index=True)

    # Ответственный за мероприятие
    responsible_employees = models.ManyToManyField(
        KsoEmployee,
        related_name='owned_events'
    )

    # Привлекаемые структурные подразделения
    attendant_departments = models.ManyToManyField(
        KsoDepartment1,
        related_name='participated_events',
        blank=True
    )

    # Параллельно привлекаемые КСО
    attendant_ksos_parallel = models.ManyToManyField(
        Kso,
        related_name='parallel_participated_events',
        blank=True
    )

    # Совместно привлекаемые КСО
    attendant_ksos_together = models.ManyToManyField(
        Kso,
        related_name='together_participated_events',
        blank=True
    )

    # Ответственное структурное подразделение
    responsible_departments = models.ManyToManyField(
        KsoDepartment1,
        related_name='owned_events'
    )

    # Тип мероприятия
    mode = models.PositiveSmallIntegerField(
        choices=EVENT_MODE_ENUM,
        blank=True, null=True
    )

    # Проект НПА
    document_project = models.TextField(blank=True, null=True)

    # Объекты контроля
    controlled_entities = models.ManyToManyField(Entity, blank=True)

    # Тип финансового контроля
    subject_performance = models.BooleanField(default=False)
    subject_financial = models.BooleanField(default=False)

    author = models.ForeignKey(
        KsoEmployee,
        on_delete=models.CASCADE, null=True, default=None, blank=True
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - {}'.format(self.exec_from, self.exec_to)

    class Meta:
        ordering = ['-exec_from']


class Workflow(models.Model):
    """
    Воркфлоу согласования документа с Event
    """

    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    # Отправитель
    sender = models.ForeignKey(
        KsoEmployee,
        related_name='workflow_sender',
        on_delete=models.CASCADE
    )

    # Получатель
    recipient = models.ForeignKey(
        KsoEmployee,
        related_name='workflow_recipient',
        on_delete=models.CASCADE
    )

    status = models.PositiveSmallIntegerField(choices=WORKFLOW_STATUS_ENUM)
    memo = models.TextField()

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']
