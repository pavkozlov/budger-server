from django.apps import AppConfig


class SchedulesConfig(AppConfig):
    name = 'budger.schedules'

    def ready(self):
        import budger.schedules.signals


default_app_config = 'budger.schedules.SchedulesConfig'
