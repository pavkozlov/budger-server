from django.db import models
from django.contrib.auth.models import User
from .entity import Entity


class Kso(models.Model):
    """
    Контрольно-счетная организация
    """
    # objects = KsoManager()

    # Наименование изображения с логотипом
    logo = models.CharField(max_length=50)

    # Название
    title_full = models.CharField(max_length=1000)
    title_short = models.CharField(max_length=1000)
    title_search = models.CharField(max_length=2001)

    # Адреса и контакты
    addr_legal = models.CharField(max_length=200)
    addr_fact = models.CharField(max_length=200)
    www = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)

    # Численность сотрудников штатная
    employees_count_staff = models.IntegerField()

    # Состоит в СМ КСО
    in_alliance = models.BooleanField()

    # Ссылка на соотв. объект контроля (юр. лицо)
    entity = models.ForeignKey(
        Entity,
        blank=True, null=True,
        on_delete=models.SET_NULL
    )

    # Руководитель
    head = models.ForeignKey(
        'KsoEmployee',
        blank=True, null=True,
        related_name='headed_kso',
        on_delete=models.SET_NULL
    )

    class Meta:
        ordering = ['title_full']

    def __str__(self):
        return '{}'.format(self.title_short)


class KsoDepartment1(models.Model):
    """ Структурное подразделение КСО первого уровня """

    # Ссылка на организацию
    kso = models.ForeignKey(
        Kso,
        on_delete=models.CASCADE,
        related_name='departments'
    )

    # Наименование
    title = models.CharField(max_length=255)

    # Может принимать участие в проведении мероприятий
    can_participate_in_events = models.BooleanField(default=False)

    # Глава
    head = models.ForeignKey(
        'KsoEmployee',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='headed_department'
    )

    # Куратор подразделения
    curator = models.ForeignKey(
        'KsoEmployee',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='curated_department'
    )

    class Meta:
        ordering = ['title']
        unique_together = ('kso', 'title',)

    def __str__(self):
        return self.title


class KsoDepartment2(models.Model):
    """ Структурное подразделение КСО второго уровня """

    # Ссылка на организацию
    kso = models.ForeignKey(
        Kso,
        on_delete=models.CASCADE
    )

    department1 = models.ForeignKey(
        KsoDepartment1,
        on_delete=models.CASCADE,
        related_name='sub_departments'
    )

    # Название
    title = models.CharField(max_length=255)

    # Глава
    head = models.ForeignKey(
        'KsoEmployee',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='headed_department2'
    )

    class Meta:
        ordering = ['title']
        unique_together = ('department1', 'title',)

    def __str__(self):
        return '{}'.format(self.title)


class KsoEmployee(models.Model):
    """
    Работник контрольно-счетной организации
    """

    # Модель пользователя
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )

    # Разработчик
    is_developer = models.BooleanField(default=False, db_index=True)

    # Работает в организации...
    kso = models.ForeignKey(
        'Kso',
        on_delete=models.CASCADE,
        related_name='employees'
    )

    # Работает в департаменте...
    department1 = models.ForeignKey(
        KsoDepartment1,
        on_delete=models.CASCADE,
        null=True, blank=True
    )

    # Работает в отделе...
    department2 = models.ForeignKey(
        KsoDepartment2,
        on_delete=models.CASCADE,
        null=True, blank=True
    )

    # Фамилия, имя, отчество
    name = models.CharField(max_length=200)

    # Должность
    position = models.CharField(max_length=200)

    # Телефон, эл. почта
    phone_landline = models.CharField(max_length=200, null=True, blank=True)
    phone_mobile = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)

    # Дата рождения
    birth_date = models.DateField(null=True, blank=True)

    # Имя файла с фотографией
    photo_slug = models.CharField(max_length=100, null=True, blank=True)

    # Может быть ответственным за мероприятие
    can_be_responsible = models.BooleanField(default=False, db_index=True)

    # Если пользоваталь отсутствует, сообщение о причине отсутствия (декрет, уход за ребенком что-то еще)
    inactive_title = models.CharField(max_length=2000, db_index=True, null=True, blank=True, default=None)

    read_only_fields = (user,)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return '{} - {}'.format(self.name, self.kso)

    def is_head(self):
        return True if self.kso.head == self else False

    def get_superiors(self):
        """Список руководителей работника КСО"""
        result = []

        if self != self.kso.head:
            if self != self.department2.head and self.department2 is not None:
                result.append(self.department2.head)

            if self.department1 is not None:
                if self != self.department1.head and self.department1.head is not None:
                    result.append(self.department1.head)

                if self != self.department1.curator and self.department1.curator is not None:
                    result.append(self.department1.curator)

            result.append(self.kso.head)

        return result
