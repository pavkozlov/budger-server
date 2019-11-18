"""
Скрипт для обновления данных о работниках КСО.
"""


def read_csv(file):
    """
    Функция принимает имя файла, возвращает список из строк файла
    :param file: file name (str)
    :return: ['row1', 'row2', 'row3', ... ]
    """
    with open(file, 'r', encoding='utf-8') as f:
        data = f.readlines()
        data.pop(0)
        print('File {} has {} rows'.format(file, len(data)))
        return data


def update(cur, data):
    """
    Функция принимает курсор для записи в БД и данные в ввиде списка
    Возвращает (id, ) если запись обновлена. None, если запись не обновлена
    :param cur:
    :param data: list()
    :return:
    """
    data.append(data[0])

    sql = '''UPDATE directory_ksoemployee SET
                id = %s, 
                name = %s,
                position = %s,
                phone_landline = %s,
                phone_mobile = %s,
                email = %s,
                birth_date = %s,
                department1_id = %s,
                department2_id = %s,
                kso_id = %s,
                user_id = %s,
                photo_slug = %s,
                is_head = %s,
                can_be_responsible = %s
            WHERE id = %s RETURNING id
    '''
    cur.execute(sql, data)
    kso_employee_id = cur.fetchone()
    return kso_employee_id


def parse_row(row):
    """
    Функция принимает строку, разделяет по ';', заменяет NULL -> None
    :param row:
    :return: list(param1, param2, param3, ...)
    """
    row_list = row.strip().split(';')
    if 'NULL' in row_list:
        for _ in range(row_list.count('NULL')):
            row_list[row_list.index('NULL')] = None
    return row_list
