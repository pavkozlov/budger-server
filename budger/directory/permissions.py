from rest_framework.permissions import BasePermission


class CanUpdateEmployee(BasePermission):
    def has_object_permission(self, request, view, obj):
        m = request.method
        u = request.user

        if m == 'PUT' and (not u.is_superuser and u.ksoemployee.id != obj.id):
            return False

        return True
