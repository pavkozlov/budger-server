from rest_framework.renderers import BaseRenderer
from budger.libs.renderers import CsvRenderer


class KsoEmployeeCsvRenderer(CsvRenderer):
    header = ['id', 'name', 'position']


class PdfRenderer(BaseRenderer):
    media_type = 'application/pdf'
    format = 'binary'
    charset = None
    render_style = 'binary'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data
