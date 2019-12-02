from rest_framework.permissions import BasePermission


class CanApproveMeeting(BasePermission):
    def has_permission(self, request, view):
        if request.user.has_perm('collegium.can_approve_meeting'):
            return True

        return False


class CanViewMeeting(BasePermission):
    def has_permission(self, request, view):
        if request.user.has_perm('collegium.view_meeting'):
            return True

        return False


class CanManageMeeting(BasePermission):
    def has_permission(self, request, view):
        if request.user.has_perm('collegium.can_manage_meeting'):
            return True

        return False
