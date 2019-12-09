from rest_framework import permissions
from .models import (
    Workflow,
    EVENT_STATUS_DRAFT,
    EVENT_STATUS_APPROVED,
    PERM_MANAGE_EVENT, PERM_ADD_EVENT
)


class CanCreateEvent(permissions.BasePermission):
    def has_object_permission(self, request, view, event):
        """
        Мероприятие можно создавать, имея спец. разрешения
        """
        if request.method == 'GET':
            if (
                request.user.is_superuser or
                request.user.has_perm(PERM_ADD_EVENT) or
                request.user.has_perm(PERM_MANAGE_EVENT)
            ):
                return True


class CanRetrieveEvent(permissions.BasePermission):
    def has_object_permission(self, request, view, event):
        """
        Мероприятие можно просмартивать когда
            - оно является согласованным, или
            - пользователь имеет специальное разрешение
            - пользователь является его автором или
            - пользователь находится в списке его согласователей.
        """
        if request.method == 'GET':
            if request.user.is_superuser or request.user.has_perm(PERM_MANAGE_EVENT):
                return True

            if event.status == EVENT_STATUS_APPROVED:
                # Мероприятие согласовано
                return True

            if event.author == request.user.ksoemployee:
                # Пользователь является автором
                return True

            # Загружаем список согласователей
            event_recipients = Workflow.objects.filter(
                event=event,
                recipient=request.user.ksoemployee
            )
            if event_recipients:
                # пользователь находится в списке его согласователей
                return True

        return False


class CanUpdateEvent(permissions.BasePermission):
    def has_object_permission(self, request, view, event):
        """
        Мероприятие можно редактировать когда
            - пользователь имеет специальное разрешение
            - оно является черновиком, а пользователь является его автором или
            - пользователь находится в списке согласователей.
        """
        if request.method in ('UPDATE', 'PATCH'):
            if request.user.is_superuser or request.user.has_perm(PERM_MANAGE_EVENT):
                return True

            if event.status == EVENT_STATUS_DRAFT:
                if event.author == request.user.ksoemployee:
                    # Пользователь является автором
                    return True

                # Загружаем список согласователей
                event_recipients = Workflow.objects.filter(
                    event=event,
                    recipient=request.user.ksoemployee
                )
                if event_recipients:
                    # пользователь находится в списке его согласователей
                    return True

        return False


class CanDeleteEvent(permissions.BasePermission):
    def has_object_permission(self, request, view, event):
        """
        Мероприятие можно удалить только если оно является черновиком.
        """
        if request.method == 'DELETE':
            if event.status == EVENT_STATUS_DRAFT and (
                request.user.is_superuser or
                request.user.has_perm(PERM_MANAGE_EVENT) or
                request.user.ksoemployee == event.author
            ):
                return True

        return False
