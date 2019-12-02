from rest_framework import generics
from .models import Job
from .serializers import JobSerializer
from .permissions import CanViewJobs


class JobListView(generics.ListAPIView):
    serializer_class = JobSerializer
    queryset = Job.objects.using('jobs').all()
    permission_classes = [CanViewJobs,]
