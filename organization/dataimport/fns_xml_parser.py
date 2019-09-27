import xml.dom.minidom
from datetime import date


def str_to_date(s):
    if s:
        d_int = [int(i) for i in s.split('-')]
        return date(*d_int)
    return None


def x_attr(elem, xpath, **kwargs):
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
    """ Returns dict with model data """

    model = {
        'reg_date': str_to_date(x_attr(elem, 'СвОбрЮЛ/@ДатаОГРН'))
    }

    if not model['reg_date']:
        return None

    model['title_full'] = x_attr(elem, 'СвНаимЮЛ/@НаимЮЛПолн')
    model['title_short'] = x_attr(elem, 'СвНаимЮЛ/@НаимЮЛСокр') or model['title_full']

    model['opf_full'] = x_attr(elem, '@ПолнНаимОПФ')
    model['opf_short'] = x_attr(elem, '@КодОПФ')

    model['inn'] = x_attr(elem, '@ИНН')
    model['kpp'] = x_attr(elem, '@КПП')
    model['ogrn'] = x_attr(elem, '@ОГРН')

    model['addr_index'] = x_attr(elem, 'СвАдресЮЛ/АдресРФ/@Индекс')

    model['addr_region_code'] = x_attr(elem, 'СвАдресЮЛ/АдресРФ/@КодРегион')
    model['addr_region_type'] = x_attr(elem, 'СвАдресЮЛ/АдресРФ/Регион/@ТипРегион', max_len=50)
    model['addr_region_title'] = x_attr(elem, 'СвАдресЮЛ/АдресРФ/Регион/@НаимРегион', max_len=50)

    region_type = x_attr(elem, 'СвАдресЮЛ/АдресРФ/Регион/@ТипРегион', max_len=50)

    if region_type == 'ГОРОД':
        model['addr_locality_type'] = 'ГОРОД'
        model['addr_locality_title'] = model['addr_region_title']
    else:
        model['addr_locality_type'] = x_attr(elem, 'СвАдресЮЛ/АдресРФ/Город/@ТипГород')
        model['addr_locality_title'] = x_attr(elem, 'СвАдресЮЛ/АдресРФ/Город/@НаимГород', max_len=50)

    if not model['addr_locality_title']:
        model['addr_locality_type'] = x_attr(elem, 'СвАдресЮЛ/АдресРФ/НаселПункт/@ТипНаселПункт', max_len=50)
        model['addr_locality_title'] = x_attr(elem, 'СвАдресЮЛ/АдресРФ/НаселПункт/@НаимНаселПункт', max_len=50)

    model['addr_street'] = x_attr(elem, 'СвАдресЮЛ/АдресРФ/Улица/@НаимУлица', max_len=50)
    model['addr_building'] = x_attr(elem, 'СвАдресЮЛ/АдресРФ/@Дом', max_len=50)
    model['addr_housing'] = x_attr(elem, 'СвАдресЮЛ/АдресРФ/@Корпус', max_len=50)
    model['addr_office'] = x_attr(elem, 'СвАдресЮЛ/АдресРФ/@Кварт', max_len=50)

    model['head_position'] = x_attr(elem, 'СведДолжнФЛ/СвДолжн/@НаимДолжн')
    model['head_name_last'] = x_attr(elem, 'СведДолжнФЛ/СвФЛ/@Фамилия')
    model['head_name_first'] = x_attr(elem, 'СведДолжнФЛ/СвФЛ/@Имя')
    model['head_name_second'] = x_attr(elem, 'СведДолжнФЛ/СвФЛ/@Отчество')

    model['head_accession_date'] = str_to_date(x_attr(elem, 'СведДолжнФЛ/СвДолжн/ГРНДата/@ДатаЗаписи'))

    return model


if __name__ == '__main__':
    with open('EGRUL_FULL_2019-01-01_385809.XML', 'r') as xml_file:
        doc = xml.dom.minidom.parse(xml_file)
        root_elem = doc.documentElement
        elements = root_elem.getElementsByTagName('СвЮЛ')
        for elem in elements:
            model = parse_elem(elem)
