from rest_framework.permissions import BasePermission


class CanViewJobs(BasePermission):
    code = 'view_jobs'

    def has_permission(self, request, view):
        u = request.user

        if u.has_perm(self.code):
            return True

        return False
