from django.db import models
from django.contrib.postgres.fields import ArrayField
from budger.directory.models.kso import KsoEmployee
from .permission import (
    PERM_MANAGE_MEETING,
    PERM_APPROVE_MEETING,
    PERM_USE_MEETING
)

MEETING_STATUS_DRAFT = 1
MEETING_STATUS_APPROVING = 2
MEETING_STATUS_PUBLISHED = 3
MEETING_STATUS_ENUM = [
    (MEETING_STATUS_DRAFT, 'Черновик'),
    (MEETING_STATUS_APPROVING, 'На согласовании'),
    (MEETING_STATUS_PUBLISHED, 'Согласовано'),
]


class Meeting(models.Model):
    # Дата проведения заседания
    exec_date = models.DateTimeField(unique=True, db_index=True)

    # Статус согласования плана заседания
    status = models.PositiveSmallIntegerField(choices=MEETING_STATUS_ENUM, default=MEETING_STATUS_DRAFT)

    class Meta:
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
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='speakers')

    # Докладчик
    employee = models.ForeignKey(KsoEmployee, on_delete=models.CASCADE)

    # Вопросы докладчика
    subjects = ArrayField(models.TextField(), null=True, blank=True)

    class Meta:
        ordering = ['id']
