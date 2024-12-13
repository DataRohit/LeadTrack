# Imports
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from apps.core.constants import ROLE_CHOICES

# Custom User Model
User = get_user_model()


# User Signup Form
class SignupForm(UserCreationForm):
    """User Signup Form.

    Inherits:
        UserCreationForm

    Attributes:
        username (str): Username
        email (str): Email
        first_name (str): First Name
        last_name (str): Last Name
        role (str): Role

    Meta:
        model (User): User
        fields (list): Fields

    Methods:
        clean_email: Check if email is already in use.
        clean_username: Check if username is already in use.
    """

    # Attributes
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Username"}
        ),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Email"}
        ),
    )
    first_name = forms.CharField(
        label="First Name",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "First Name"}
        ),
    )
    last_name = forms.CharField(
        label="Last Name",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Last Name"}
        ),
    )
    role = forms.ChoiceField(
        label="Role",
        choices=ROLE_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
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
            "password1",
            "password2",
        ]

    # Method to clean email
    def clean_email(self) -> str:
        """Check if email is already in use.

        Returns:
            str: Email
        """

        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email is already in use.")
        return email

    def clean_username(self) -> str:
        """Check if username is already in use.

        Returns:
            str: Username
        """

        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username is already in use.")
        return username


# User Login Form
class LoginForm(forms.Form):
    """User Login Form.

    Inherits:
        forms.Form

    Attributes:
        email (str): Email
        password (str): Password

    Meta:
        model (User): User
        fields (list): Fields

    Methods:
        clean: Check if username and password are correct.
    """

    # Attributes
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Email"}
        ),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        ),
    )

    # Meta class
    class Meta:
        # Attributes
        model = User
        fields = ["email", "password"]

    # Method to clean
    def clean(self) -> dict:
        """Check if username and password are correct.

        Returns:
            dict: Form data
        """

        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user = User.objects.filter(email=email).first()
        if user and not user.check_password(password):
            raise ValidationError("Invalid email or password.")
        return self.cleaned_data
