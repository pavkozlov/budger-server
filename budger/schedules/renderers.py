from rest_framework import renderers


class EsgfkXmlRenderer(renderers.BaseRenderer):
    media_type = 'application/xml'
    format = '.xml'

    @staticmethod
    def _render_model(model):
        xml = f'<title>{model.title}</title>'
        return f'<model>{xml}</model>'

    def render(self, data, media_type=None, renderer_context=None):
        xml = ''

        for model in data:
            xml += self._render_model(model)

        return '<?xml version="1.0"?>\n<root>{}</root>'.format(xml)
