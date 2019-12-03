from django.apps import AppConfig


class DirectoryConfig(AppConfig):
    name = 'budger.directory'

    def ready(self):
        import budger.directory.signals


default_app_config = 'budger.directory.DirectoryConfig'
