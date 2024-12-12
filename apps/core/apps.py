# Imports
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


# CoreConfig Class
class CoreConfig(AppConfig):
    """CoreConfig

    CoreConfig class is used to configure the core app.

    Inherits:
        AppConfig

    Attributes:
        name (str): The name of the app.
        verbose_name (str): The verbose name of the app.
    """

    # Attributes
    name = "apps.core"
    verbose_name = _("Core")
