import os
from django.apps import AppConfig

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        # Import scheduler and start it
        from .scheduler import start_scheduler
        if os.getenv("ENABLE_SCHEDULER", "true").lower() == "true":
            start_scheduler()