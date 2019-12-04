from rest_framework.permissions import BasePermission


class CanUpdateUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        m = request.method
        u = request.user

        if m == 'PUT' and (not u.is_superuser and u.id != obj.id):
            return False

        return True
