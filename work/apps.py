from django.apps import AppConfig


class WorkConfig(AppConfig):
    name = 'work'

    def ready(self):
        import work.signals
