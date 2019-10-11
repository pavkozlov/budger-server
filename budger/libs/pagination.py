import sys
from rest_framework.pagination import PageNumberPagination


class UnlimitedResultsSetPagination(PageNumberPagination):
    page_size = sys.maxsize
