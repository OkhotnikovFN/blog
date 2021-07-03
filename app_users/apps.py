from django.apps import AppConfig


class AppUsersConfig(AppConfig):
    name = 'app_users'

    def ready(self):
        import app_users.signals
