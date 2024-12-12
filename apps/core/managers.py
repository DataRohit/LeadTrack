# Imports
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _

from apps.core.constants import ROLE_CHOICES


# UserManager Class
class UserManager(DjangoUserManager["User"]):  # type: ignore
    """UserManager

    UserManager class for the User model.

    Inherits:
        DjangoUserManager["User"]
    """

    # _create_user Method
    def _create_user(
        self, email: str, password: str | None, role: str = "sales", **extra_fields
    ) -> "User":  # type: ignore # noqa: F821
        """_create_user

        Creates a user with the given email and password.

        Args:
            email (str): The user's email.
            password (str | None): The user's password.
            role (str): The user's role.
            **extra_fields: Extra fields to be passed to the User model.

        Returns:
            User: The created user.
        """

        if not email:
            raise ValueError(_("The Email field must be set."))
        email = self.normalize_email(email)
        validate_email(email)

        valid_roles = [choice[0] for choice in ROLE_CHOICES]
        if role not in valid_roles:
            raise ValueError(
                _("Invalid role. Allowed roles are: {}.").format(", ".join(valid_roles))
            )

        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # create_user Method
    def create_user(
        self,
        email: str,
        password: str | None = None,
        role: str = "sales",
        **extra_fields,
    ) -> "User":  # type: ignore # noqa: F821
        """create_user

        Creates a user with the given email and password.

        Args:
            email (str): The user's email.
            password (str | None): The user's password.
            role (str): The user's role.
            **extra_fields: Extra fields to be passed to the User model.

        Returns:
            User: The created user.
        """

        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, role, **extra_fields)

    # create_superuser Method
    def create_superuser(
        self,
        email: str,
        password: str | None = None,
        role: str = "admin",
        **extra_fields,
    ) -> "User":  # type: ignore # noqa: F821
        """create_superuser

        Creates a superuser with the given email and password.

        Args:
            email (str): The user's email.
            password (str | None): The user's password.
            role (str): The user's role.
            **extra_fields: Extra fields to be passed to the User model.

        Returns:
            User: The created superuser.
        """

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        role = "admin"

        return self._create_user(email, password, role, **extra_fields)
