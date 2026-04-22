from django.apps import AppConfig


class AccueilConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accueil"
    verbose_name = "Contenu du site EMSP"

    def ready(self):
        # Import signals so receivers are connected at startup.
        from . import signals  # noqa: F401
