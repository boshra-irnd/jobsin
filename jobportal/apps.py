from django.apps import AppConfig


class JobportalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'jobportal'
    
    def ready(self) -> None:
        import jobportal.signals
