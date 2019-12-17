from rest_framework import views
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.response import Response
from .data import NatProject, RegProject


class NatProjectsView(views.APIView):
    """
    GET Список национальных проектов.
    """
    def get(self, request):
        return Response(NatProject.list())


class RegProjectsView(views.APIView):
    """
    GET Список региональных проектов.
    """
    def get(self, request, *args, **kwargs):
        if kwargs.get('pk') is not None:
            # Вернуть данные о выбранном регпроекте
            p = RegProject.get_by_id(kwargs['pk'])
            if p:
                return Response(p)

        return Response(status=HTTP_404_NOT_FOUND)
