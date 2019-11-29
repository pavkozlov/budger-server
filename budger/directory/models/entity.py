from django.db import models
from django.contrib.postgres.fields import ArrayField


ORG_TYPE_ENUM = [
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
    # TODO unique=True
    ofk_regnum = models.CharField(max_length=5, db_index=True)

    # Код организации (обособленного подразделения) по Сводному реестру, присваиваемый в ОрФК
    # TODO unique=True
    ofk_code = models.CharField(max_length=8, db_index=True)

    # Ссылка на вышестоящую организацию (вычисляется по полю "Код вышестоящего УБП по Сводному реестру")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    # Дата регистрации
    reg_date = models.DateField(null=True, blank=True)

    # Дата прекращения
    term_date = models.DateField(null=True, blank=True)

    # Наименование и код ОПФ
    opf_title = models.CharField(max_length=250, null=True, blank=True)
    opf_code = models.CharField(max_length=5, null=True, blank=True, db_index=True)

    # Код и Наименование по ОКФС
    okfs_title = models.CharField(max_length=250)
    okfs_code = models.CharField(max_length=2)

    # Код и наименование КБК
    kbk_title = models.CharField(max_length=2000, null=True, blank=True)
    kbk_code = models.CharField(max_length=3, null=True, blank=True)

    # Код и наименование типа организации
    org_type_code = models.CharField(max_length=2, choices=ORG_TYPE_ENUM)

    # Наименование ЮЛ
    title_full = models.CharField(max_length=2000, db_index=True)
    title_short = models.CharField(max_length=2000, null=True, blank=True)

    # ИНН, КПП, ОГРН
    inn = models.CharField(max_length=12, null=True, blank=True, db_index=True)
    kpp = models.CharField(max_length=9, null=True, blank=True)
    ogrn = models.CharField(max_length=13, null=True, blank=True)

    # Справочник ОКТМО
    oktmo_code = models.CharField(max_length=11, null=True, blank=True)
    oktmo_title = models.CharField(max_length=500, null=True, blank=True)

    # Адрес
    addr_index = models.CharField(max_length=6, null=True, blank=True)

    # Регион
    addr_area_type = models.CharField(max_length=10, blank=True, null=True)
    addr_area_title = models.CharField(max_length=1000, blank=True, null=True)

    # Населенный пункт: тип, наименование
    addr_locality_type = models.CharField(max_length=10, blank=True, null=True)
    addr_locality_title = models.CharField(max_length=1000, blank=True, null=True)

    # Улица, дом, корпус, ОФИС
    addr_street = models.CharField(max_length=1011, null=True, blank=True)
    addr_building = models.CharField(max_length=50, null=True, blank=True)
    addr_housing = models.CharField(max_length=50, null=True, blank=True)
    addr_office = models.CharField(max_length=50, null=True, blank=True)

    # Руководитель
    head_position = models.CharField(max_length=300, null=True, blank=True)
    head_name = models.CharField(max_length=200, null=True, blank=True)
    head_accession_date = models.DateField(null=True, blank=True)

    # Код статуса организации.
    org_status_code = models.CharField(max_length=1, choices=ORG_STATUS_ENUM, db_index=True)

    # Код наименования специального мероприятия в отношении организации.
    spec_event_code = models.CharField(max_length=1, choices=SPEC_EVENT_CODE_ENUM, null=True, blank=True)

    # Код бюджета организации
    budget_code = models.CharField(max_length=8, db_index=True, null=True, blank=True)
    budget_title = models.CharField(max_length=2000, null=True, blank=True)

    # Код уровня бюджета
    budget_lvl_code = models.CharField(max_length=2, choices=BUDGET_LVL_CODE_ENUM, db_index=True, null=True, blank=True)

    # Код по справочнику ОКОГУ.
    okogu_code = models.CharField(max_length=7, db_index=True, null=True, blank=True)

    # Подчиненные огранизации (по версии РУБП)
    subordinates = ArrayField(models.IntegerField(), blank=True, null=True)

    # Служебные поля
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    title_search = models.CharField(max_length=4001, default='', db_index=True)

    # Дата акруальности данных
    relevance_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['title_full']

    def __str__(self):
        return '{} - {}'.format(self.inn, self.title_full)


class MunicipalBudget(models.Model):
    title_original = models.CharField(max_length=2000)
    title_display = models.CharField(max_length=2000, db_index=True, null=True, blank=True)
    code = models.CharField(max_length=8, db_index=True)

    # Следующий уровень муниципального дерева ОК
    subordinates = ArrayField(models.IntegerField(), blank=True, null=True)

    class Meta:
        ordering = ['title_display']

    def __str__(self):
        return self.title_display
