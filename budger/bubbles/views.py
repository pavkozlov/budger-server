from rest_framework import views
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.response import Response
from .data import NatProject, RegProject
from budger.directory.models.entity import Entity


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

        if request.query_params.get('_filter__grbs'):
            grbs_id = request.query_params.get('_filter__grbs')
            try:
                grbs = Entity.objects.get(id=grbs_id)
                grbs_title = grbs.title_full
                p_list = RegProject.get_by_grbs(grbs_title)
                return Response([RegProject.transform(p) for p in p_list])
            except Entity.DoesNotExist:
                return Response(status=HTTP_404_NOT_FOUND)

        return Response(status=HTTP_404_NOT_FOUND)
