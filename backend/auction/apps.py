from django.apps import AppConfig
import sys


class AuctionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auction'
    
    def ready(self, *args, **kwargs):
        is_manage_py = any(arg.casefold().endswith("manage.py") for arg in sys.argv)
        is_runserver = any(arg.casefold() == "runserver" for arg in sys.argv)

        if is_manage_py and is_runserver:
            from .mqtt_client import start_mqtt
            start_mqtt()
