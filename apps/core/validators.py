# Imports
from django.core import validators
from django.utils.translation import gettext_lazy as _


# Custom Username Validator
class UsernameValidator(validators.RegexValidator):
    """UsernameValidator

    Custom Username Validator to validate the username field in the User model.

    Inherits:
        RegexValidator

    Attributes:
        regex (str): Regular expression to validate the username.
        message (str): Error message to display if the username is invalid.
        flags (int): Flags to be passed to the re.compile() function.
    """

    regex = r"^[A-Za-z][A-Za-z0-9@_-]*$"
    message = _(
        "Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters."
    )
    flags = 0
