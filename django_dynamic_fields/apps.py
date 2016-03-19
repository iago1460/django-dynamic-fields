from django.apps import AppConfig
from django.core.exceptions import AppRegistryNotReady, FieldError
from django.db.utils import ProgrammingError
from django_dynamic_fields.utils import update_schemas


class ProjectConfig(AppConfig):
    name = 'django_dynamic_fields'

    def ready(self):
        import django_dynamic_fields.signals
        try:
            update_schemas()
        except (AppRegistryNotReady, FieldError, ProgrammingError):
            pass
