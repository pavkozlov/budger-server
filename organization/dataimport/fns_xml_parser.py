"""
Библиотечка для разбора XML из ФНС.
"""


import xml.dom.minidom
from datetime import date


def str_to_date(s):
    """ Принимает строку, отдает Date"""
    if s:
        d_int = [int(i) for i in s.split('-')]
        return date(*d_int)
    return None


def x_attr(elem, xpath, **kwargs):
    """
    Возвращает атрибут элемента
    :param elem: Обрабатываемый элемент.
    :param xpath: XPath до атрибута.
    :param kwargs: max_len - задается максимальная длина значения атрибута.
    :return:
    """
    _elem, _attr_name = None, None

    if xpath and len(xpath) >= 2:
        if '/' in xpath:
            tokens = xpath.split('/')
            _els = elem.getElementsByTagName(tokens.pop(0))
            if _els:
                _elem = _els[0]
                _attr_name = None
                while tokens and _elem and not _attr_name:
                    token = tokens.pop(0)
                    if token[0] == '@':
                        _attr_name = token[1:]
                    else:
                        _els = _elem.getElementsByTagName(token)
                        _elem = _els[0] if _els else None
        elif xpath[0] == '@':
            _elem = elem
            _attr_name = xpath[1:]

    if _elem and _attr_name and _attr_name in _elem.attributes:
        value = _elem.attributes[_attr_name].nodeValue
        if 'max_len' in kwargs:
            if kwargs['max_len'] < len(value):
                print('Value {} has overlength.'.format(value))
        return _elem.attributes[_attr_name].nodeValue

    # TODO: MUST return None in the real script
    return ''


def parse_elem(elem):
    """ Возвращает dict с данными модели """

    _model = {
        'reg_date': str_to_date(x_attr(elem, 'СвОбрЮЛ/@ДатаОГРН'))
    }

    if not _model['reg_date']:
        return None

    _model['title_full'] = x_attr(elem, 'СвНаимЮЛ/@НаимЮЛПолн')
    _model['title_short'] = x_attr(elem, 'СвНаимЮЛ/@НаимЮЛСокр') or _model['title_full']

    _model['opf_full'] = x_attr(elem, '@ПолнНаимОПФ')
    _model['opf_short'] = x_attr(elem, '@КодОПФ')

    _model['inn'] = x_attr(elem, '@ИНН')
    _model['kpp'] = x_attr(elem, '@КПП')
    _model['ogrn'] = x_attr(elem, '@ОГРН')

    _model['addr_index'] = x_attr(elem, 'СвАдресЮЛ/АдресРФ/@Индекс')

    _model['addr_region_code'] = x_attr(elem, 'СвАдресЮЛ/АдресРФ/@КодРегион')
    _model['addr_region_type'] = x_attr(elem, 'СвАдресЮЛ/АдресРФ/Регион/@ТипРегион', max_len=50)
    _model['addr_region_title'] = x_attr(elem, 'СвАдресЮЛ/АдресРФ/Регион/@НаимРегион', max_len=50)

    region_type = x_attr(elem, 'СвАдресЮЛ/АдресРФ/Регион/@ТипРегион', max_len=50)

    if region_type == 'ГОРОД':
        _model['addr_locality_type'] = 'ГОРОД'
        _model['addr_locality_title'] = _model['addr_region_title']
    else:
        _model['addr_locality_type'] = x_attr(elem, 'СвАдресЮЛ/АдресРФ/Город/@ТипГород')
        _model['addr_locality_title'] = x_attr(elem, 'СвАдресЮЛ/АдресРФ/Город/@НаимГород', max_len=50)

    if not _model['addr_locality_title']:
        _model['addr_locality_type'] = x_attr(elem, 'СвАдресЮЛ/АдресРФ/НаселПункт/@ТипНаселПункт', max_len=50)
        _model['addr_locality_title'] = x_attr(elem, 'СвАдресЮЛ/АдресРФ/НаселПункт/@НаимНаселПункт', max_len=50)

    _model['addr_street'] = x_attr(elem, 'СвАдресЮЛ/АдресРФ/Улица/@НаимУлица', max_len=50)
    _model['addr_building'] = x_attr(elem, 'СвАдресЮЛ/АдресРФ/@Дом', max_len=50)
    _model['addr_housing'] = x_attr(elem, 'СвАдресЮЛ/АдресРФ/@Корпус', max_len=50)
    _model['addr_office'] = x_attr(elem, 'СвАдресЮЛ/АдресРФ/@Кварт', max_len=50)

    _model['head_position'] = x_attr(elem, 'СведДолжнФЛ/СвДолжн/@НаимДолжн')
    _model['head_name_last'] = x_attr(elem, 'СведДолжнФЛ/СвФЛ/@Фамилия')
    _model['head_name_first'] = x_attr(elem, 'СведДолжнФЛ/СвФЛ/@Имя')
    _model['head_name_second'] = x_attr(elem, 'СведДолжнФЛ/СвФЛ/@Отчество')

    _model['head_accession_date'] = str_to_date(x_attr(elem, 'СведДолжнФЛ/СвДолжн/ГРНДата/@ДатаЗаписи'))

    return _model


if __name__ == '__main__':
    with open('EGRUL_FULL_2019-01-01_385809.XML', 'r', encoding='utf-8') as xml_file:
        doc = xml.dom.minidom.parse(xml_file)
        root_elem = doc.documentElement
        elements = root_elem.getElementsByTagName('СвЮЛ')
        for elem in elements:
            model = parse_elem(elem)
