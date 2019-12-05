from rest_framework.permissions import BasePermission

# Создание и редактирование черновиков
PERM_MANAGE_EVENT = 'schedules.manage_event'

# Согласование мероприятия
PERM_APPROVE_EVENT = 'schedules.approve_event'

# Просмотр согласованного мероприятия
PERM_USE_EVENT = 'schedules.use_event'

# Просмотр всех согласований
PERM_VIEWALL_WORKFLOW = 'schedules.viewall_workflow'


class CanViewAllWorkflows(BasePermission):
    code = 'view_all_workflows'

    def has_permission(self, request, view):
        if request.user.has_perm(self.code):
            return True

        return False


class CanViewOwnWorkflows(BasePermission):
    def has_permission(self, request, view):
        current_employee_id = request.user.ksoemployee.id
        recipient_id = request.data.get('_filter__recipient_id', None)

        if current_employee_id == recipient_id:
            return True

        return False
