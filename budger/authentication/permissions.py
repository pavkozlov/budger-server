from rest_framework.permissions import BasePermission


class CanViewUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        u = request.user

        if u.is_superuser or u.id == obj.id:
            return True

        return False


class CanUpdateUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        m = request.method
        u = request.user

        if m == 'PUT' and (not u.is_superuser and u.id != obj.id):
            return False

        return True


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        id1 = obj.employee.id
        id2 = request.user.ksoemployee.id

        if id1 == id2:
            return True

        return False

    def has_permission(self, request, view):
        request_employee_id = request.user.ksoemployee.id
        m = request.method

        if m == 'POST' and request.data.get('employee') and int(request.data.get('employee')) != request_employee_id:
            return False

        return True
