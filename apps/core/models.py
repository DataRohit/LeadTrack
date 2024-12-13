# Imports
import uuid
from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from apps.core.constants import ROLE_CHOICES, TOKEN_TYPES
from apps.core.managers import UserManager
from apps.core.validators import UsernameValidator


# Customer User Model
class User(AbstractUser):
    """Customer User Model

    Custom User model for the application.

    Inherits:
        AbstractUser

    Attributes:
        pkid (models.BigAutoField): The primary key of the user.
        id (models.UUIDField): The UUID of the user.
        first_name (models.CharField): The first name of the user.
        last_name (models.CharField): The last name of the user.
        username (models.CharField): The username of the user.
        email (models.EmailField): The email of the user.

    Constants:
        EMAIL_FIELD (str): The email field of the user.
        USERNAME_FIELD (str): The username field of the user.
        REQUIRED_FIELDS (list[str]): The required fields for the user.

    Managers:
        objects (UserManager): The object manager of the user

    Meta:
        verbose_name (str): The verbose name of the user.
        verbose_name_plural (str): The verbose name of the user in plural.
        ordering (list[str]): The ordering of the user.

    Properties:
        full_name (str): The full name of the user.
    """

    # Attributes
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    first_name = models.CharField(_("first name"), max_length=30, blank=True)
    last_name = models.CharField(_("last name"), max_length=30, blank=True)
    username = models.CharField(
        _("username"),
        max_length=24,
        unique=True,
        help_text=_(
            "Required. 24 characters or fewer. Letters, digits and @/-/_ only."
        ),
        validators=[UsernameValidator()],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_("email address"), unique=True)
    role = models.CharField(
        _("Role"),
        max_length=24,
        choices=ROLE_CHOICES,
        default=ROLE_CHOICES[0][0],
    )

    # Set the email and username fields
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"

    # Set the required fields
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    # Set object manager
    objects = UserManager()

    # Meta class
    class Meta:
        # Attributes
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ["-date_joined"]

        indexes = [
            models.Index(fields=["id"], name="user_id_idx"),
            models.Index(fields=["username"], name="user_username_idx"),
            models.Index(fields=["email"], name="user_email_idx"),
        ]

    # Property to get the full name
    @property
    def full_name(self) -> str:
        """Get the full name of the user.

        Returns:
            str: The full name of the user.
        """
        return f"{self.first_name} {self.last_name}".strip()


# Token Record Model
class TokenRecord(models.Model):
    """Token Record Model

    Token record model for the application.

    Inherits:
        models.Model

    Attributes:
        user (models.ForeignKey): The user of the token.
        token_type (models.CharField): The type of the token.
        token (models.CharField): The token.
        created_at (models.DateTimeField): The created date of the token.
        is_used (models.BooleanField): The used status of the token.

    Properties:
        is_expired (bool): The expired status of the token.
    """

    # Attributes
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tokens")
    token_type = models.CharField(
        max_length=24, choices=TOKEN_TYPES, default=TOKEN_TYPES[0][0]
    )
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    # Method to get the expired status of the token
    @property
    def is_expired(self, expiry_duration=timedelta(hours=1)):
        # Return the expired status
        return now() > self.created_at + expiry_duration
