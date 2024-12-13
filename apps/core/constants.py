# Imports
from django.utils.translation import gettext_lazy as _

# Role Choices
ROLE_CHOICES = (
    ("admin", _("Admin")),
    ("manager", _("Manager")),
    ("sales", _("Sales")),
    ("support", _("Support")),
)

# Token Types
TOKEN_TYPES = (
    ("activation", _("Activation")),
    ("reset_password", _("Reset Password")),
)
