""" Simple library for employees JSON parser. """


def x_departments(rec: dict):
    """
    Формирование данных о структурных подразделениях из файла kso_employees.json: departament1 и departament2
    Логика следующая: в каждой записи имеются поля inspection и otdel.
        Если определены inspection и otdel, то departament1, departament2 = inspection, otdel
        Если определен только otdel, то departament1, departament2 = otdel, None
        Если не определена ни одна переменная, то departament1, departament2 = None, None
    """

    inspection = rec.get('inspection', '').strip()
    inspection = None if inspection == '' else inspection

    otdel = rec.get('otdel', '').strip()
    otdel = None if otdel == '' else otdel

    department1 = inspection
    department2 = otdel

    if department1 is None:
        department1 = otdel
        department2 = None

    return department1, department2
