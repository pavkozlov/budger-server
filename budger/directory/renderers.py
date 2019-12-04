from budger.libs.renderers import CsvRenderer


class KsoEmployeeCsvRenderer(CsvRenderer):
    header = ['id', 'name', 'position']
