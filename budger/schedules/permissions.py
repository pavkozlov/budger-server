from rest_framework.permissions import BasePermission


class CanViewAllWorkflows(BasePermission):
    def has_permission(self, request, view):

        if request.user.has_perm('schedules.view_all_workflows'):
            return True

        return False


class CanViewOwnWorkflows(BasePermission):
    def has_permission(self, request, view):
        current_employee_id = request.user.ksoemployee.id
        recipient_id = request.data.get('_filter__recipient_id', None)

        if current_employee_id == recipient_id:
            return True

        return False
