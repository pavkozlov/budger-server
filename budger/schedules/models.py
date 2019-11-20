from django.db import models
from budger.directory.models.entity import Entity
from budger.directory.models.kso import Kso, KsoDepartment1, KsoEmployee


ANNUAL_STATUS_ENUM = [
    (1, 'В работе'),
    (2, 'На согласовании'),
    (3, 'Согласовано'),
]

EVENT_STATUS_ENUM = [
    (1, 'В работе'),
    (2, 'На согласовании'),
    (3, 'Согласовано'),
]

EVENT_TYPE_ENUM = [
    (1, 'Контрольное'),
    (3, 'Экспертно-аналитическое'),
    (2, 'Экспертное'),
]

EVENT_MODE_ENUM = [
    (2, 'Самостоятельное'),
    (1, 'Совместное мероприятие'),
    (3, 'Параллельное мероприятие'),
]

EVENT_INITIATOR_ENUM = [
    (1, 'Руководитель субъекта РФ (муниципального образования)'),
    (2, 'Законодательный орган субъекта РФ (муниципального образования)'),
    (3, 'Счетная палата РФ'),
    (4, 'Правоохранителные органы'),
    (5, 'Гражданин'),
    (6, 'Общественная организация'),
    (7, 'КСП Московской области'),
]

EVENT_SUBJECT_ENUM = [
    (1, 'Финансовый аудит'),
    (2, 'Аудит эффективности'),
]


class Annual(models.Model):
    year = models.PositiveSmallIntegerField(db_index=True)
    status = models.PositiveSmallIntegerField(db_index=True, choices=ANNUAL_STATUS_ENUM)

    def __str__(self):
        return '{} - {}'.format(self.year, self.status)

    class Meta:
        ordering = ['-year']


class Event(models.Model):
    # Статус мероприятия
    status = models.PositiveSmallIntegerField(db_index=True, choices=EVENT_STATUS_ENUM, blank=True, null=True)

    # Вид мероприятия
    type = models.PositiveSmallIntegerField(db_index=True, choices=EVENT_TYPE_ENUM)

    # Наименование мероприятия
    title = models.CharField(max_length=255)

    # Проверяемый период
    period_from = models.DateField(db_index=True)
    period_to = models.DateField(db_index=True)

    # Даты проведения мероприятия
    exec_from = models.DateField(db_index=True)
    exec_to = models.DateField(db_index=True)

    # Ответственный за мероприятие
    responsible_employee = models.ForeignKey(
        KsoEmployee,
        on_delete=models.DO_NOTHING,
        related_name='owned_events'
    )

    # Привлекаемые структурные подразделения
    attendant_departments = models.ManyToManyField(
        KsoDepartment1,
        related_name='participated_events',
        blank=True
    )

    # Ответственное структурное подразделение
    responsible_department = models.ForeignKey(
        KsoDepartment1,
        related_name='owned_events',
        on_delete=models.DO_NOTHING,
        null=True, blank=True
    )

    # Тип мероприятия
    mode = models.PositiveSmallIntegerField(
        choices=EVENT_MODE_ENUM,
        blank=True, null=True
    )

    # Тип финансового контроля
    subject = models.PositiveSmallIntegerField(
        choices=EVENT_SUBJECT_ENUM,
        null=True, blank=True
    )

    # Примечание
    notes = models.TextField(null=True, blank=True)

    # Обоснование включения в план
    memo = models.TextField(null=True, blank=True)

    # Привлекаемые внешние организации (эксперты)
    attendant_experts = models.TextField(null=True)

    # Объекты контроля
    controlled_entities = models.ManyToManyField(Entity, blank=True)

    # КСО, принимающие участие в мероприятии (когда тип мероприятия параллельный или совместный)
    attendant_ksos = models.ManyToManyField(Kso, blank=True)

    # Инициатор поручения/обращения, реквизиты письма
    initiator = models.PositiveSmallIntegerField(
        db_index=True,
        choices=EVENT_INITIATOR_ENUM,
        blank=True, null=True
    )
    letter_number = models.CharField(max_length=20, blank=True, null=True)
    letter_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return '{} - {}'.format(self.exec_from, self.exec_to)

    class Meta:
        ordering = ['-exec_from']
