from rest_framework.permissions import BasePermission


class CanViewJobs(BasePermission):
    CODE = 'can_view_jobs'

    def has_permission(self, request, view):
        u = request.user

        if u.has_perm(self.CODE):
            return True

        return False
