from django.db import models
from budger.directory.models.entity import Entity
from budger.directory.models.kso import Kso, KsoDepartment1, KsoEmployee
from django.contrib.postgres.fields import ArrayField

ANNUAL_STATUS_ENUM = [
    (1, 'В работе'),
    (2, 'На согласовании'),
    (3, 'Согласовано'),
]

EVENT_STATUS_ENUM = [
    (10, 'Черновик'),
    (20, 'Согласовано руководителем отдела'),
    (30, 'Согласовано руководителем департамента'),
    (40, 'Согласовано Председателем КСО'),
]

EVENT_TYPE_ENUM = [
    (1, 'Контрольное'),
    (2, 'Экспертно-аналитическое'),
    (3, 'Экспертное'),
]

EVENT_SUBJECT_ENUM = [
    (1, 'Финансовый аудит (контроль)'),
    (2, 'Аудит в сфере закупок'),
    (3, 'Аудит эффективности'),
    (4, 'Экспертиза проекта закона'),
    (5, 'Финансово-экономическая экспертиза')
]

EVENT_MODE_ENUM = [
    (1, 'Самостоятельное мероприятие'),
    (2, 'Совместное мероприятие'),
    (3, 'Параллельное мероприятие'),
]

WORKFLOW_STATUS_ENUM = [
    (1, 'Черновик'),
    (2, 'Согласовано начальником инспекции'),
    (3, 'Согласовано аудитором'),
    (4, 'Согласовано Председателем'),
]

EVENT_INITIATOR_ENUM = [
    (1, 'По предложениям Губернатора Московской области / Главы муниципального образования'),
    (2, 'По поручениям Московской областной думы / Законодательного органа муниципального образования'),
    (3, 'По обращениям граждан'),
    (4, 'По обращениям общественных организаций'),
    (5, 'По обращениям правоохранительных органов'),
    (6, 'По решению Совета КСО МО'),
    (7, 'По решению органа аудита (контроля)'),
    (8, 'По обращениям Правительства Московской области / Администрации муниципального образования'),
]

EVENT_SUBTYPE_ENUM = [
    (1, 'С оценкой рисков возникновения коррупционных проявлений'),
    (2, 'С проверкой реализации приоритетных и национальных проектов'),
    (3, 'С проверкой соблюдения порядка управления и распоряжения имуществом'),
    (4, 'С проверкой порядка и условий предоставления межбюджетных трансфертов'),
]

EVENT_WAY_ENUM = [
    (1, 'С выездом'),
    (2, 'Камерально')
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

    # Дополнительные признаки
    subtype = models.PositiveSmallIntegerField(choices=EVENT_SUBTYPE_ENUM, blank=True, null=True)

    # Тип мероприятия
    subject = ArrayField(
        models.PositiveSmallIntegerField(choices=EVENT_SUBJECT_ENUM),
        null=True,
        blank=True,
        default=None
    )

    # Наименование мероприятия
    title = models.CharField(max_length=255)

    # Основания для проведения мероприятия
    initiator = models.PositiveSmallIntegerField(choices=EVENT_INITIATOR_ENUM, null=True, blank=True)

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
