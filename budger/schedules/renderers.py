from rest_framework import renderers


class EsgfkXmlRenderer(renderers.BaseRenderer):
    media_type = 'application/xml'
    format = '.xml'

    @staticmethod
    def _render_model(model):
        xml = '<title>{}</title>'.format(model.title)
        return '<model>{}</model>'.format(xml)

    def render(self, data, media_type=None, renderer_context=None):
        xml = ''

        for model in data:
            xml += self._render_model(model)

        return '<?xml version="1.0"?>\n<root>{}</root>'.format(xml)
