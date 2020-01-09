from django.db import models
from django.contrib.postgres.fields import ArrayField
from budger.directory.models.kso import KsoEmployee
from .permission import (
    PERM_MANAGE_MEETING,
    PERM_APPROVE_MEETING,
    PERM_USE_MEETING
)

MEETING_STATUS_DRAFT = 1
MEETING_STATUS_IN_WORK = 2
MEETING_STATUS_APPROVED = 3
MEETING_STATUS_ENUM = [
    (MEETING_STATUS_DRAFT, 'Черновик'),
    (MEETING_STATUS_IN_WORK, 'На согласовании'),
    (MEETING_STATUS_APPROVED, 'Согласовано'),
]


class Meeting(models.Model):
    # Дата проведения заседания
    exec_date = models.DateTimeField('Дата проведения заседания', unique=True, db_index=True)

    # Статус согласования плана заседания
    status = models.PositiveSmallIntegerField('Статус согласования плана заседания', choices=MEETING_STATUS_ENUM,
                                              default=MEETING_STATUS_DRAFT)

    class Meta:
        verbose_name = 'Заседание'
        verbose_name_plural = 'Заседания'
        ordering = ['exec_date']
        permissions = [
            (
                PERM_MANAGE_MEETING.split('.')[1],
                'Создание, редактирование и отправка на согласование черновика плана заседания.'
            ),
            (
                PERM_APPROVE_MEETING.split('.')[1],
                'Согласование плана заседания.'
            ),
            (
                PERM_USE_MEETING.split('.')[1],
                'Просмотр согласованного плана заседания.'
            ),
        ]

    def __str__(self):
        return '{}'.format(self.exec_date)


class Speaker(models.Model):
    # Ключ сортировки
    id = models.BigAutoField(primary_key=True)

    # Встреча
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='speakers', verbose_name='Встреча')

    # Докладчик
    employee = models.ForeignKey(KsoEmployee, on_delete=models.CASCADE, verbose_name='Докладчик')

    # Вопросы докладчика
    subjects = ArrayField(models.TextField(), null=True, blank=True, verbose_name='Вопросы докладчика')

    class Meta:
        verbose_name = 'Спикер'
        verbose_name_plural = 'Спикеры'
        ordering = ['id']
