from django.db import models
from django.contrib.postgres.fields import ArrayField

ORG_TYPE_ENUM = [
    ('01', 'фед. орган гос. власти, фед. гос. орган, орган гос. власти...'),
    ('02', 'орган управления государственным внебюджетным фондом'),
    ('03', 'учреждение'),
    ('05', 'унитарное предприятие'),
    ('09', 'государственная корпорация, государственная компания'),
    ('20', 'иные юридические лица, иные неучастники бюджетного процесса'),
    ('22', 'Центральный банк Российской Федерации (Банк России)'),
]

ORG_STATUS_ENUM = [
    ('1', 'действующая'),
    ('2', 'недействующая'),
    ('3', 'отсутствуют правоотношения'),
    ('4', 'специальные указания'),
]

SPEC_EVENT_CODE_ENUM = [
    ('1', 'реорганизация'),
    ('2', 'ликвидация'),
    ('3', 'изменение подведомственности'),
    ('4', 'изменение типа учреждения'),
    ('5', 'изменение уровня бюджета')
]

BUDGET_LVL_CODE_ENUM = [
    ('00', 'не определен'),
    ('10', 'федеральный бюджет'),
    ('20', 'бюджет субъекта Российской Федерации'),
    ('30', 'местный бюджет'),
    ('31', 'бюджет городского округа'),
    ('32', 'бюджет муниципального района'),
    ('33', 'бюджет городского поселения'),
    ('34', 'бюджет сельского поселения'),
    ('35', 'бюджет городского округа с внутригородским делением'),
    ('36', 'бюджет внутригородского муниципального образования города федерального значения'),
    ('37', 'бюджет внутригородского района'),
    ('40', 'бюджет государственного внебюджетного фонда Российской Федерации'),
    ('41', 'бюджет Пенсионного фонда Российской Федерации'),
    ('42', 'бюджет Фонда социального страхования Российской Федерации'),
    ('43', 'бюджет Федерального фонда обязательного медицинского страхования'),
    ('50', 'бюджет территориального государственного внебюджетного фонда'),
]


class Entity(models.Model):
    """
    Объект контроля.
    """

    # Учетный номер организации, присваиваемый в ОрФК
    ofk_regnum = models.CharField('Учетный номер организации, присваиваемый в ОрФК', max_length=5, db_index=True)

    # Код организации (обособленного подразделения) по Сводному реестру, присваиваемый в ОрФК
    ofk_code = models.CharField('Код организации по сводному реестру, присваиваемый в ОрФК', max_length=8,
                                db_index=True)

    # Ссылка на вышестоящую организацию (вычисляется по полю "Код вышестоящего УБП по Сводному реестру")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True,
                               verbose_name='Ссылка на вышестоящую организацию')

    # Дата регистрации
    reg_date = models.DateField('Дата регистрации', null=True, blank=True)

    # Дата прекращения
    term_date = models.DateField('Дата прекращения', null=True, blank=True)

    # Наименование и код ОПФ
    opf_title = models.CharField('Наименование ОПФ', max_length=250, null=True, blank=True)
    opf_code = models.CharField('Код ОПФ', max_length=5, null=True, blank=True, db_index=True)

    # Код и Наименование по ОКФС
    okfs_title = models.CharField('Наименование по ОКФС', max_length=250)
    okfs_code = models.CharField('Код по ОКФС', max_length=2)

    # Код и наименование КБК
    kbk_title = models.CharField('Наименование КБК', max_length=2000, null=True, blank=True)
    kbk_code = models.CharField('Код КБК', max_length=3, null=True, blank=True)

    # Код и наименование типа организации
    org_type_code = models.CharField('Код и наименование типа организации', max_length=2, choices=ORG_TYPE_ENUM)

    # Наименование ЮЛ
    title_full = models.CharField('Наименование ЮЛ', max_length=2000, db_index=True)
    title_short = models.CharField('Сокращённое наименование ЮЛ', max_length=2000, null=True, blank=True)

    # ИНН, КПП, ОГРН
    inn = models.CharField('ИНН', max_length=12, db_index=True, null=True, blank=True)
    kpp = models.CharField('КПП', max_length=9, db_index=True, null=True, blank=True)
    ogrn = models.CharField('ОГРН', max_length=13, db_index=True, null=True, blank=True)

    # Справочник ОКТМО
    oktmo_code = models.CharField('Код ОКТМО', max_length=11, null=True, blank=True)
    oktmo_title = models.CharField('Наименование ОКТМО', max_length=500, null=True, blank=True)

    # Адрес
    addr_index = models.CharField('Адрес', max_length=6, null=True, blank=True)

    # Регион
    addr_area_type = models.CharField('Тип региона', max_length=10, blank=True, null=True)
    addr_area_title = models.CharField('Наименование региона', max_length=1000, blank=True, null=True)

    # Населенный пункт: тип, наименование
    addr_locality_type = models.CharField('Тип населенного пункта', max_length=10, blank=True, null=True)
    addr_locality_title = models.CharField('Наименование населенного пункта', max_length=1000, blank=True, null=True)

    # Улица, дом, корпус, ОФИС
    addr_street = models.CharField('Улица', max_length=1011, null=True, blank=True)
    addr_building = models.CharField('Дом', max_length=50, null=True, blank=True)
    addr_housing = models.CharField('Корпус', max_length=50, null=True, blank=True)
    addr_office = models.CharField('Офис', max_length=50, null=True, blank=True)

    # Руководитель: должность, имя, дата вступления, фото
    head_position = models.CharField('Должность руководителя', max_length=300, null=True, blank=True)
    head_name = models.CharField('Имя руководителя', max_length=200, null=True, blank=True)
    head_accession_date = models.DateField('Дата вступления в должность', null=True, blank=True)
    head_photo_slug = models.CharField('Фотография', max_length=200, null=True, blank=True)

    # Код статуса организации.
    org_status_code = models.CharField('Код статуса организации', max_length=1, choices=ORG_STATUS_ENUM, db_index=True)

    # Код наименования специального мероприятия в отношении организации.
    spec_event_code = models.CharField(
        'Код наименования специального мероприятия в отношении организации',
        max_length=1,
        choices=SPEC_EVENT_CODE_ENUM,
        null=True,
        blank=True
    )

    # Код бюджета организации
    budget_code = models.CharField('Код бюджета организации', max_length=8, db_index=True, null=True, blank=True)
    budget_title = models.CharField('Наименование бюджета организации', max_length=2000, null=True, blank=True)

    # Код уровня бюджета
    budget_lvl_code = models.CharField(
        'Код уровня бюджета',
        max_length=2,
        choices=BUDGET_LVL_CODE_ENUM,
        db_index=True,
        null=True,
        blank=True
    )

    # Код по справочнику ОКОГУ.
    okogu_code = models.CharField('Код по справочнику ОКОГУ', max_length=7, db_index=True, null=True, blank=True)

    # Подчиненные огранизации (по версии РУБП)
    subordinates = ArrayField(
        models.IntegerField(),
        blank=True,
        null=True,
        verbose_name='Подчиненные огранизации (по версии РУБП)'
    )

    # Служебные поля
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    title_search = models.CharField(max_length=4001, default='', db_index=True)

    # Дата акруальности данных
    relevance_date = models.DateTimeField('Дата акруальности данных', null=True, blank=True)

    # Признак, указывающий, является ли организация Органом государственной власти.
    is_ogv = models.BooleanField('Является ли организация органом государственной власти', default=False, db_index=True)

    class Meta:
        ordering = ['title_full']
        verbose_name = 'Объект контроля'
        verbose_name_plural = '5. Объекты контроля'

    def __str__(self):
        return '{} - {}'.format(self.inn, self.title_full)


class MunicipalBudget(models.Model):
    title_original = models.CharField(max_length=2000)
    title_display = models.CharField(max_length=2000, db_index=True, null=True, blank=True)
    code = models.CharField(max_length=8, db_index=True)

    # Следующий уровень муниципального дерева ОК
    subordinates = ArrayField(models.IntegerField(), blank=True, null=True)

    administration = models.ForeignKey(
        Entity,
        blank=True, null=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        ordering = ['title_display']

    def __str__(self):
        return self.title_display


class EntityGroup(models.Model):
    """
    Кэширование информации о группировке объектов контроля по различным признакам.
    """
    code = models.CharField(max_length=100, db_index=True, unique=True)
    data = ArrayField(models.IntegerField())
