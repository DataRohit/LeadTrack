# Imports
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from apps.core.forms import UserChangeForm, UserCreationForm
from apps.core.models import User


# Register the User model
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """User Admin

    User Admin for the User model.

    Inherits:
        BaseUserAdmin

    Attributes:
        list_display (list[str]): The list of fields to display.
        list_display_links (list[str]): The list of fields to display as links.
        search_fields (list[str]): The list of fields to search.
        ordering (list[str]): The list of fields to order by.
        fieldsets (tuple[str]): The fieldsets for the User model.
        add_fieldsets (tuple[str]): The add fieldsets for the User model.
    """

    # Set model
    model = User

    # Set forms
    add_form = UserCreationForm
    form = UserChangeForm

    # List display
    list_display = [
        "pkid",
        "id",
        "email",
        "first_name",
        "last_name",
        "username",
        "is_active",
        "role",
    ]

    # List display links
    list_display_links = ["pkid", "id", "email"]

    # Search fields
    search_fields = ["email", "first_name", "last_name", "username", "role"]

    # List filter
    list_filter = ["is_active", "is_staff", "is_superuser", "role"]

    # Ordering
    ordering = ["-date_joined"]

    # Fieldsets
    fieldsets = (
        (_("User Profile"), {"fields": ("pkid", "id")}),
        (_("Login Credentials"), {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "username")}),
        (
            _("Permissions and Groups"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "role",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important Dates"), {"fields": ("last_login", "date_joined")}),
    )

    # Add fieldsets
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "username",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    # Set readonly fields
    readonly_fields = ["pkid", "id", "last_login", "date_joined"]
