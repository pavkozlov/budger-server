from rest_framework import generics, views
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, FileUploadParser

from budger.directory.models.kso import Kso

from .models import Job
from .serializers import JobSerializer
from .permissions import CanViewJobs
from .renderers import KsoCsvRenderer


class JobListView(generics.ListAPIView):
    serializer_class = JobSerializer
    queryset = Job.objects.using('jobs').all()
    permission_classes = [CanViewJobs,]


class KsoImportExportView(views.APIView):
    """
    GET CSV
    PUT
    """
    def get_renderers(self):
        if self.request.method == 'GET':
            return KsoCsvRenderer(),
        else:
            return JSONRenderer(),

    def get_parsers(self):
        if self.request.method == 'PUT':
            return FileUploadParser(),
        else:
            return JSONParser(),

    def get(self, request):
        recs = Kso.objects.all()

        data = [
            {
                'id': rec.id,
                'title_short': rec.title_short,
                'www': rec.www,
                'email': rec.email,
                'phone': rec.phone,
                'addr_fact': rec.addr_fact,
                'employees_count_staff': rec.employees_count_staff,
                'in_alliance': rec.in_alliance

            } for rec in recs
        ]

        return Response(
            data,
            headers={'Content-Disposition': 'attachment; filename="kso.csv"'}
        )

    def put(self, request):
        file_obj = request.data['file']
        return Response(status=204)
