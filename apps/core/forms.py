# Imports
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from apps.core.models import User


# User Creation Form
class UserCreationForm(forms.ModelForm):
    """User Creation Form

    A form for creating new users. Includes all the required
    fields, plus repeated password validation.

    Inherits:
        forms.ModelForm

    Attributes:
        password1 (forms.CharField): The first password field.
        password2 (forms.CharField): The repeated password field.

    Meta:
        model (User): The user model.
        fields (list[str]): The fields to include in the form.

    Methods:
        clean_password2: Validates that the two password fields match.
        save: Saves the user instance with the hashed password.
    """

    # Attributes
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        help_text="Enter a secure password.",
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput,
        help_text="Enter the same password as above, for verification.",
    )

    # Meta class
    class Meta:
        # Attributes
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
        ]

    # Method to clean the user's password
    def clean_username(self):
        """Validate that the username is unique.

        Returns:
            str: The cleaned username.

        Raises:
            forms.ValidationError: If the username is not unique.
        """

        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username is already taken.")
        return username

    # Method to clean the user's email
    def clean_email(self):
        """Validate that the email is unique.

        Returns:
            str: The cleaned email.

        Raises:
            forms.ValidationError: If the email is not unique.
        """

        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already taken.")
        return email

    def clean_password2(self):
        """Validate that the two passwords match.

        Returns:
            str: The cleaned password.

        Raises:
            forms.ValidationError: If the passwords do not match.
        """

        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2

    def save(self, commit=True):
        """Save the user instance with the hashed password.

        Args:
            commit (bool, optional): Whether to save the instance. Defaults to True.

        Returns:
            User: The saved user instance.
        """

        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


# User Change Form
class UserChangeForm(forms.ModelForm):
    """User Change Form

    A form for updating users. Includes all fields, but replaces the password
    field with admin's password hash display field.

    Inherits:
        forms.ModelForm

    Attributes:
        password (ReadOnlyPasswordHashField): A display field for hashed passwords.

    Meta:
        model (User): The user model.
        fields (list[str]): The fields to include in the form.

    Methods:
        clean_password: Returns the initial password value.
    """

    # Attributes
    password = ReadOnlyPasswordHashField(
        label="Password",
        help_text=(
            "Raw passwords are not stored, so there is no way to see this user's password. "
            "You can change the password using <a href='../password/'>this form</a>."
        ),
    )

    # Meta class
    class Meta:
        # Attributes
        model = User
        fields = [
            "email",
            "username",
            "first_name",
            "last_name",
            "role",
            "password",
            "is_active",
            "is_staff",
            "is_superuser",
        ]

    def clean_password(self):
        """Return the initial password value.

        Returns:
            str: The initial password value.
        """

        return self.initial["password"]
