# Imports
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


# AccountsConfig Class
class AccountsConfig(AppConfig):
    """AccountsConfig

    AccountsConfig class is used to configure the accounts app.

    Inherits:
        AppConfig

    Attributes:
        name (str): The name of the app.
        verbose_name (str): The verbose name of the app.
    """

    # Attributes
    name = "apps.accounts"
    verbose_name = _("Accounts")
