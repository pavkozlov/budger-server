from django.db import models
from budger.directory.models.entity import Entity
from budger.directory.models.kso import Kso, KsoDepartment1, KsoEmployee
from budger.libs.shortcuts import get_object_or_none
from django.contrib.postgres.fields import ArrayField


# Создание, редактирование и удаление черновиков
PERM_MANAGE_EVENT = 'schedules.manage_event'

# Встроенное
PERM_ADD_EVENT = 'schedules.add_event'

# Просмотр всех согласований
PERM_MANAGE_WORKFLOW = 'schedules.manage_workflow'


ANNUAL_STATUS_ENUM = [
    (1, 'В работе'),
    (2, 'На согласовании'),
    (3, 'Согласовано'),
]

EVENT_STATUS_DRAFT = 10
EVENT_STATUS_IN_WORK = 20
EVENT_STATUS_APPROVED = 30

EVENT_STATUS_ENUM = [
    (EVENT_STATUS_DRAFT, 'Черновик'),
    (EVENT_STATUS_IN_WORK, 'В работе'),
    (EVENT_STATUS_APPROVED, 'Согласовано'),
]

EVENT_TYPE_ENUM = [
    (1, 'Контрольное мероприятие'),
    (2, 'Экспертно-аналитическое мероприятие'),
    (3, 'Экспертиза проекта НПА'),
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

WORKFLOW_STATUS_IN_WORK = 0
WORKFLOW_STATUS_ACCEPTED = 1
WORKFLOW_STATUS_REJECTED = 2

WORKFLOW_STATUS_ENUM = [
    (WORKFLOW_STATUS_IN_WORK, 'В работе'),
    (WORKFLOW_STATUS_ACCEPTED, 'Согласовано'),
    (WORKFLOW_STATUS_REJECTED, 'Отклонено'),
]

'''
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
'''

EVENT_INITIATOR_ENUM = [
    (1, 'Предложение Губернатора Московской области'),
    (2, 'Поручение Московской областной думы'),
    (3, 'Обращение Правительства Московской области / Администрации муниципального образования'),
    (4, 'Обращение граждан'),
    (5, 'Обращение общественных организаций'),
    (6, 'Обращение правоохранительных органов'),
    (7, 'Решение Совета КСО МО'),
    (8, 'Решение органа аудита (контроля)'),
]

EVENT_SUBTYPE_ENUM = [
    (1, 'Оценка рисков возникновения коррупционных проявлений'),
    (2, 'Проверка реализации приоритетных и национальных проектов'),
    (3, 'Проверка соблюдения порядка управления и распоряжения имуществом'),
    (4, 'Проверка порядка и условий предоставления межбюджетных трансфертов'),
]

EVENT_WAY_ENUM = [
    (1, 'С выездом'),
    (2, 'Камерально')
]


class Annual(models.Model):
    year = models.PositiveSmallIntegerField(db_index=True)

    status = models.PositiveSmallIntegerField(
        db_index=True,
        choices=ANNUAL_STATUS_ENUM
    )

    def __str__(self):
        return '{} - {}'.format(self.year, self.status)

    class Meta:
        ordering = ['-year']


class Event(models.Model):
    # Порядковый номер мероприятия
    number = models.SmallIntegerField(blank=True, null=True, db_index=True)

    # Статус мероприятия
    status = models.PositiveSmallIntegerField(
        db_index=True,
        choices=EVENT_STATUS_ENUM,
        default=EVENT_STATUS_DRAFT,
        blank=True,
        null=True
    )

    # Вид мероприятия
    type = models.PositiveSmallIntegerField(db_index=True, choices=EVENT_TYPE_ENUM)

    # Дополнительные признаки
    subtype = ArrayField(models.PositiveSmallIntegerField(choices=EVENT_SUBTYPE_ENUM), blank=True, null=True)

    # Тип мероприятия
    subject = ArrayField(models.PositiveSmallIntegerField(
        choices=EVENT_SUBJECT_ENUM),
        size=3,
        null=True,
        blank=True,
        default=None
    )

    # Наименование мероприятия
    title = models.CharField(max_length=2000)

    # Основания для проведения мероприятия
    initiators = ArrayField(models.PositiveSmallIntegerField(choices=EVENT_INITIATOR_ENUM), null=True, blank=True)

    # Проверяемый период
    period_from = models.DateField(db_index=True, null=True, blank=True)
    period_to = models.DateField(db_index=True, null=True, blank=True)

    # Метод проведения
    method = models.CharField(max_length=250, null=True, blank=True, db_index=True)

    # Способ проведения
    way = ArrayField(models.PositiveSmallIntegerField(db_index=True, choices=EVENT_WAY_ENUM), null=True, blank=True)

    # Даты проведения мероприятия
    exec_from = models.DateField(db_index=True)
    exec_to = models.DateField(db_index=True)

    # Ответственный за мероприятие
    responsible_employees = models.ManyToManyField(
        KsoEmployee,
        related_name='owned_events'
    )

    # Ответственный за мероприятие
    responsible_employee = models.ForeignKey(
        KsoEmployee,
        on_delete=models.CASCADE,
        blank=True, null=True,
        related_name='responded_events'
    )

    # Ответственное структурное подразделение
    responsible_department = models.ForeignKey(
        KsoDepartment1,
        on_delete=models.CASCADE,
        blank=True, null=True,
        related_name='responded_events'
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

    # Форма проведения
    mode = models.PositiveSmallIntegerField(
        choices=EVENT_MODE_ENUM,
        blank=True, null=True
    )

    # Проект НПА
    document_project = models.TextField(blank=True, null=True)

    # Объекты контроля
    controlled_entities = models.ManyToManyField(Entity, blank=True)

    # Работник, создавший мероприятие
    author = models.ForeignKey(KsoEmployee, on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - {}'.format(self.exec_from, self.exec_to)

    class Meta:
        ordering = ['number']
        permissions = [
            (PERM_MANAGE_EVENT.split('.')[1], 'Создание и редактирование черновиков.'),
        ]


class Workflow(models.Model):
    """
    Воркфлоу согласования документа с Event.
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

    status = models.PositiveSmallIntegerField(
        choices=WORKFLOW_STATUS_ENUM,
        default=WORKFLOW_STATUS_IN_WORK,
        db_index=True
    )

    memo = models.TextField(null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = [
            (PERM_MANAGE_WORKFLOW.split('.')[1], 'Управление согласованиями.'),
        ]
        ordering = ['created']

    def get_next_link_model(self):
        """
        Создание нового согласования на основе предыдущего.

        Логика следующая:
            - Если предыдуший WF согласован, следующий WF отправляется на согласование начальнику.
            - Если предыдуший WF отклонен, следующий WF отправляется на доработку предыдущему отправителю.

        ВНИМАНИЕ!
        ЕСЛИ после текущего WF уже имеются согласования, ничего не предпринимается.
        """

        if not self.id:
            return None

        # Если WF не последний в цепочке, не делаем ничего
        next_workflow = Workflow.objects.filter(
            id__gt=self.id,
            event=self.event,
            sender=self.recipient,
        )[:1]
        if next_workflow:
            return None

        if self.status == WORKFLOW_STATUS_ACCEPTED:
            # Согоасование согласована, создаем WF, направленный следующему из superiors.
            superiors = self.recipient.get_superiors()
            if len(superiors) > 0:
                new_recipient = get_object_or_none(KsoEmployee, pk=superiors[0].id)
                if new_recipient:
                    return Workflow(
                        event=self.event,
                        sender=self.recipient,
                        recipient=new_recipient
                    )

        if self.status == WORKFLOW_STATUS_REJECTED:
            # Согласование отклонено, передаем эстафету направившеиу "кривую" версию.
            last_accepted_workflow = Workflow.objects.filter(
                event=self.event,
                recipient=self.recipient,
                status=WORKFLOW_STATUS_ACCEPTED
            ).order_by('-created')[:1]
            if last_accepted_workflow:
                recipient = last_accepted_workflow[0].sender
            else:
                recipient = self.sender

            return Workflow(
                event=self.event,
                sender=self.recipient,
                recipient=recipient
            )
