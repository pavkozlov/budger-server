from rest_framework import renderers
import io
import csv
from abc import ABC


class CsvRenderer(renderers.BaseRenderer, ABC):
    media_type = 'text/plain'
    format = 'csv'
    header = []

    def _generate_row(self, row):
        new_row = {}
        for h in self.header:
            new_row[h] = row.get(h)
        return new_row

    def render(self, data, media_type=None, renderer_context=None):
        results = data.get('results')

        if results is not None and type(self.header) is list and len(self.header) > 0:
            output = io.StringIO()
            csv_writer = csv.DictWriter(output, fieldnames=self.header, delimiter='\t')
            csv_writer.writeheader()

            for row in results:
                csv_writer.writerow(self._generate_row(row))

            return output.getvalue()
        else:
            return []
