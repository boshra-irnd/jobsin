from django.apps import AppConfig


class JobsearchConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'jobsearch'
    
    def ready(self) -> None:
        import jobsearch.signals
