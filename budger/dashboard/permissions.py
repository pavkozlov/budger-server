from rest_framework.permissions import BasePermission


VIEW_JOBS = 'view_jobs'


class CanViewJobs(BasePermission):

    def has_permission(self, request, view):
        u = request.user

        if u.has_perm(VIEW_JOBS):
            return True

        return False
