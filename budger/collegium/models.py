from django.db import models
from django.contrib.postgres.fields import ArrayField
from budger.directory.models.kso import KsoEmployee

COLLEGIUM_STATUS_DRAFT = 1
COLLEGIUM_STATUS_APPROVED = 3
COLLEGIUM_STATUS_ENUM = [
    (COLLEGIUM_STATUS_DRAFT, 'Черновик'),
    (2, 'На согласовании'),
    (COLLEGIUM_STATUS_APPROVED, 'Согласовано'),
]


class Meeting(models.Model):
    # Дата проведения
    exec_date = models.DateTimeField(unique=True, db_index=True)

    # Статус встречи
    status = models.PositiveSmallIntegerField(choices=COLLEGIUM_STATUS_ENUM, default=COLLEGIUM_STATUS_DRAFT)

    class Meta:
        ordering = ['exec_date']
        permissions = [
            ("can_manage_meeting", "Can manage meeting."),
            ("can_approve_meeting", "Can approve meeting.")
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