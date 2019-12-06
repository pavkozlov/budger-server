from rest_framework.permissions import BasePermission

# Создание и редактирование черновиков
PERM_MANAGE_EVENT = 'schedules.manage_event'

# Согласование мероприятия
PERM_APPROVE_EVENT = 'schedules.approve_event'

# Просмотр согласованного мероприятия
PERM_USE_EVENT = 'schedules.use_event'

# Просмотр всех согласований
PERM_MANAGE_WORKFLOW = 'schedules.manage_workflow'
