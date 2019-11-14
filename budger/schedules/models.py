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
    (2, 'Экспертное'),
    (3, 'Экспертно-аналитическое'),
]

EVENT_MODE_ENUM = [
    (2, 'Самостоятельное'),
    (1, 'Совместное'),
    (3, 'Параллельное'),
]

EVENT_FORM_ENUM = [
    (1, 'Плановая'),
    (2, 'Внеплановая'),
]

EVENT_INSPECTION_ENUM = [
    (1, 'Внешний государственный (муниципальный) финансовый контроль'),
    (2, 'Внутренний государственный (муниципальный) финансовый контроль'),
    (3, 'Внутренний аудит объектов контроля Счетной палаты'),
]

EVENT_METHOD_ENUM = [
    (1, 'Обследование'),
    (2, 'Проверка'),
]

EVENT_REASON_ENUM = [
    (1, 'По инициативе контрольного органа'),
    (2, 'По поручениям и обращениям'),
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

EVENT_FINANCIAL_CONTROL_ENUM = [
    (1, 'Финансовый аудит (контроль)'),
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
    # ВАЖНО: коллега пользователя, формирующего мероприятие
    responsible_employee = models.ForeignKey(
        KsoEmployee,
        on_delete=models.DO_NOTHING,
        related_name='owned_events'
    )

    # Привлекаемые структурные подразделения
    # ВАЖНО: подразделения КСО, где работает пользователь, формирующий мероприятие
    attendant_departments = models.ManyToManyField(
        KsoDepartment1,
        related_name='participated_events',
        blank=True
    )

    # Ответственное структурное подразделение
    # ВАЖНО: подразделение КСО, где работает пользователь, формирующий мероприятие
    responsible_department = models.ForeignKey(
        KsoDepartment1,
        related_name='owned_events',
        on_delete=models.DO_NOTHING, null=True, blank=True
    )

    # Тип мероприятия
    mode = models.PositiveSmallIntegerField(db_index=True, choices=EVENT_MODE_ENUM, blank=True, null=True)

    # Вид контроля
    inspection = models.PositiveSmallIntegerField(db_index=True, choices=EVENT_INSPECTION_ENUM)

    # Форма мероприятия
    form = models.PositiveSmallIntegerField(db_index=True, choices=EVENT_FORM_ENUM)

    # Метод проведения мероприятия
    method = models.PositiveSmallIntegerField(db_index=True, choices=EVENT_METHOD_ENUM, blank=True, null=True)

    # Основание мероприятия
    reason = models.PositiveSmallIntegerField(db_index=True, choices=EVENT_REASON_ENUM)

    # Инициатор поручений/обращений
    initiator = models.PositiveSmallIntegerField(db_index=True, choices=EVENT_INITIATOR_ENUM, null=True)

    # Тип финансового контроля
    financial_control = models.PositiveSmallIntegerField(db_index=True, choices=EVENT_FINANCIAL_CONTROL_ENUM)

    # Примечание
    note = models.TextField(null=True)

    # Привлекаемые внешние организации (эксперты)
    attendant_experts = models.TextField(null=True)

    # Фонд рабочего времени (человекочасы)
    working_time = models.PositiveSmallIntegerField(blank=True, null=True)

    # Объект контроля
    controlled_entities = models.ManyToManyField(Entity, db_index=True)

    # КСО, принимающие участие в мероприятии (когда тип мероприятия параллельный или совместный)
    attendant_kso = models.ManyToManyField(Kso, db_index=True, blank=True)

    # Реквизиты обращения
    appeal_author = models.CharField(max_length=200, db_index=True, blank=True, null=True)
    appeal_number = models.CharField(max_length=50, db_index=True, blank=True, null=True)
    appeal_date = models.DateField(db_index=True, blank=True, null=True)

    def __str__(self):
        return '{} - {}'.format(self.exec_from, self.exec_to)

    class Meta:
        ordering = ['-exec_from']
