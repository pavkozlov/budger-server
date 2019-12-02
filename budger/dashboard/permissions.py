from rest_framework.permissions import BasePermission


class CanViewJobs(BasePermission):
    CODE = 'dashboard.can_view_jobs'

    def has_permission(self, request, view):
        u = request.user

        if u.has_perm(self.CODE):
            return True

        return False
