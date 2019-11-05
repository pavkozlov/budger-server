from rest_framework.permissions import BasePermission


class CanListDepartment(BasePermission):
    def has_permission(self, request, view):
        m = request.method
        u = request.user

        if m == 'GET' and u.has_perm('t.view_department'):
            return True

        return False


class CanAddDepartment(BasePermission):
    def has_permission(self, request, view):
        m = request.method
        u = request.user

        if m == 'POST' and u.has_perm('t.add_department'):
            return True

        return False
