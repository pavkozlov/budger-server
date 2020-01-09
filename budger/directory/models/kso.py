from django.db import models
from django.contrib.auth.models import User
from .entity import Entity


class Kso(models.Model):
    """
    Контрольно-счетная организация
    """
    # objects = KsoManager()

    # Наименование изображения с логотипом
    logo = models.CharField('Наименование изображения с логотипом', max_length=50)

    # Название
    title_full = models.CharField('Полное наименование', max_length=1000)
    title_short = models.CharField('Сокращённое наименование', max_length=1000)
    title_search = models.CharField(max_length=2001)

    # Адреса и контакты
    addr_legal = models.CharField('Юридический адрес', max_length=200)
    addr_fact = models.CharField('Фактический адрес', max_length=200)
    www = models.CharField('Сайт', max_length=100, blank=True, null=True)
    email = models.CharField('Email', max_length=100)
    phone = models.CharField('Телефон', max_length=100)

    # Численность сотрудников штатная
    employees_count_staff = models.IntegerField('Штатная численность сотрудников')

    # Состоит в СМ КСО
    in_alliance = models.BooleanField('Состоит в СМ КСО')

    # Ссылка на соотв. объект контроля (юр. лицо)
    entity = models.ForeignKey(
        Entity,
        blank=True, null=True,
        on_delete=models.SET_NULL,
        verbose_name='Объект контроля (юр. лицо)'
    )

    # Руководитель
    head = models.ForeignKey(
        'KsoEmployee',
        blank=True, null=True,
        related_name='headed_kso',
        on_delete=models.SET_NULL,
        verbose_name='Руководитель'
    )

    class Meta:
        ordering = ['title_full']
        verbose_name = 'Контрольно-счетная организация'
        verbose_name_plural = '1. Контрольно-счетные организации'

    def __str__(self):
        return '{}'.format(self.title_short)


class KsoDepartment1(models.Model):
    """ Структурное подразделение КСО первого уровня """

    # Ссылка на организацию
    kso = models.ForeignKey(
        Kso,
        on_delete=models.CASCADE,
        related_name='departments',
        verbose_name='Ссылка на организацию'
    )

    # Наименование
    title = models.CharField('Наименование', max_length=255)

    # Может принимать участие в проведении мероприятий
    can_participate_in_events = models.BooleanField('Может принимать участие в проведении мероприятий', default=False)

    # Глава
    head = models.ForeignKey(
        'KsoEmployee',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='headed_department',
        verbose_name='Глава подразделения'
    )

    # Куратор подразделения
    curator = models.ForeignKey(
        'KsoEmployee',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='curated_department',
        verbose_name='Куратор подразделения'
    )

    class Meta:
        ordering = ['title']
        unique_together = ('kso', 'title',)
        verbose_name = 'Структурное подразделение КСО первого уровня'
        verbose_name_plural = '3. Структурные подразделения КСО первого уровня'

    def __str__(self):
        return self.title


class KsoDepartment2(models.Model):
    """ Структурное подразделение КСО второго уровня """

    # Ссылка на организацию
    kso = models.ForeignKey(
        Kso,
        on_delete=models.CASCADE,
        verbose_name='Ссылка на организацию'
    )

    department1 = models.ForeignKey(
        KsoDepartment1,
        on_delete=models.CASCADE,
        related_name='sub_departments',
        verbose_name='Структурное подразделение КСО первого уровня'
    )

    # Название
    title = models.CharField('Название', max_length=255)

    # Глава
    head = models.ForeignKey(
        'KsoEmployee',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='headed_department2',
        verbose_name='Глава'
    )

    class Meta:
        ordering = ['title']
        unique_together = ('department1', 'title',)
        verbose_name = 'Структурное подразделение КСО второго уровня'
        verbose_name_plural = '4. Структурные подразделения КСО второго уровня'

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
        null=True, blank=True,
        verbose_name='Пользователь'
    )

    # Разработчик
    is_developer = models.BooleanField('Разработчик', default=False, db_index=True)

    # Работает в организации...
    kso = models.ForeignKey(
        'Kso',
        on_delete=models.CASCADE,
        related_name='employees',
        verbose_name='КСО'
    )

    # Работает в департаменте...
    department1 = models.ForeignKey(
        KsoDepartment1,
        on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name='Департамент'
    )

    # Работает в отделе...
    department2 = models.ForeignKey(
        KsoDepartment2,
        on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name='Отдел'
    )

    # Фамилия, имя, отчество
    name = models.CharField('ФИО', max_length=200)

    # Должность
    position = models.CharField('Должность', max_length=200)

    # Телефон, эл. почта
    phone_landline = models.CharField('Стационарный телефон', max_length=200, null=True, blank=True)
    phone_mobile = models.CharField('Мобильный телефон', max_length=200, null=True, blank=True)
    email = models.CharField('Email', max_length=200, null=True, blank=True)

    # Дата рождения
    birth_date = models.DateField('Дата рождения', null=True, blank=True)

    # Имя файла с фотографией
    photo_slug = models.CharField(max_length=100, null=True, blank=True)

    # Может быть ответственным за мероприятие
    can_be_responsible = models.BooleanField('Может быть ответственным за мероприятие', default=False, db_index=True)

    # Если пользоваталь отсутствует, сообщение о причине отсутствия (декрет, уход за ребенком что-то еще)
    inactive_title = models.CharField(
        'Причина отсутствия',
        max_length=2000,
        db_index=True,
        null=True,
        blank=True,
        default=None
    )

    read_only_fields = (user,)

    class Meta:
        ordering = ['name']
        verbose_name = 'Работник контрольно-счетной организации'
        verbose_name_plural = '2. Работники контрольно-счетных организаций'

    def __str__(self):
        return '{} - {}'.format(self.name, self.kso)

    def is_head(self):
        return True if self.kso.head == self else False

    def get_superiors(self):
        """Список руководителей работника КСО"""
        result = []

        if self != self.kso.head:
            if self.department2 is not None and self != self.department2.head:
                result.append(self.department2.head)

            if self.department1 is not None:
                if self.department1.head is not None and self != self.department1.head:
                    result.append(self.department1.head)

                if self.department1.curator is not None and self != self.department1.curator:
                    result.append(self.department1.curator)

            result.append(self.kso.head)

        return result
