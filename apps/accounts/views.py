# Imports
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import View

from apps.accounts.forms import LoginForm, SignupForm
from apps.core.models import TokenRecord

# User Model
User = get_user_model()


# Signup View
class SignupView(View):
    """User Signup View with Email Verification.

    Inherits:
        View

    Methods:
        get: Method to handle get request
        post: Method to handle post request
    """

    # Method to handle get request
    def get(self, request):
        # Initialize the form
        form = SignupForm()

        # Render the signup page
        return render(request, "accounts/signup.html", {"form": form})

    # Method to handle post request
    def post(self, request):
        # Initialize the form
        form = SignupForm(request.POST)

        # Check if the form is valid
        if form.is_valid():
            # Create a new user
            user = form.save(commit=False)

            # Set the user as inactive
            user.is_active = False

            # Save the user
            user.save()

            # Create new token and uid
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Create user activation link
            activation_link = request.build_absolute_uri(
                f"/accounts/activate/{uid}/{token}/"
            )

            # Send the activation email
            send_mail(
                "Activate Your Account",
                f"Click the link to verify your email: {activation_link}",
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )

            # Create a new token record
            TokenRecord.objects.create(user=user, token_type="activation", token=token)

            # Add success message
            messages.success(
                request,
                "Account Activation Mail Sent Successfully!",
                extra_tags="success",
            )

            # Redirect to the login page
            return redirect("accounts:login")

        # Traverse through the form errors
        for _, error_list in form.errors.items():
            # Get the errors
            for error in error_list:
                # Add error message
                messages.error(request, error, extra_tags="danger")

        # Render the signup page
        return render(request, "accounts/signup.html", {"form": form})


# User Activation View
class ActivateView(View):
    """User Activation View.

    Inherits:
        View

    Methods:
        get: Method to handle get request
    """

    # Method to handle get request
    def get(self, request, uidb64, token):
        # Decode the uid
        uid = force_str(urlsafe_base64_decode(uidb64))

        # Get the user
        user = get_object_or_404(User, pk=uid)

        # Get the token record
        token_record = TokenRecord.objects.filter(
            user=user, token_type="activation", token=token
        ).first()

        # If the token record is not found or is used or is expired
        if not token_record or token_record.is_used or token_record.is_expired:
            # Add error message
            messages.error(request, "Activation Link is Invalid!", extra_tags="danger")

            # Redirect to the login page
            return redirect("accounts:login")

        # Check if the token is valid
        if default_token_generator.check_token(user, token):
            # Render the activation page
            return render(
                request,
                "accounts/activate.html",
                {"user": user, "uidb64": uidb64, "token": token},
            )

        # Add error message
        messages.error(request, "Activation Link is Invalid!", extra_tags="danger")

        # Redirect to the login page
        return redirect("accounts:login")

    # Method to handle post request
    def post(self, request, uidb64, token):
        # Decode the uid
        uid = force_str(urlsafe_base64_decode(uidb64))

        # Get the user
        user = get_object_or_404(User, pk=uid)

        # Get the token record
        token_record = TokenRecord.objects.filter(
            user=user, token_type="activation", token=token
        ).first()

        # If the token record is not found or is used or is expired
        if not token_record or token_record.is_used or token_record.is_expired:
            # Add error message
            messages.error(request, "Activation Link is Invalid!", extra_tags="danger")

            # Redirect to the login page
            return redirect("accounts:login")

        # Check if the token is valid
        if default_token_generator.check_token(user, token):
            # Activate the user and save
            user.is_active = True
            user.save()

            # Update and save the token record
            token_record.is_used = True
            token_record.save()

            # Add success message
            messages.success(
                request, "Account Activated Successfully!", extra_tags="success"
            )

            # Redirect to the login page
            return redirect("accounts:login")

        # Add error message
        messages.error(request, "Activation Link is Invalid!", extra_tags="danger")

        # Redirect to the login page
        return redirect("accounts:login")


# User Login View
class LoginView(View):
    """User Login View.

    Inherits:
        View

    Methods:
        get: Method to handle get request
    """

    # Method to handle get request
    def get(self, request):
        # Initialize the form
        form = LoginForm()

        # Render the login page
        return render(request, "accounts/login.html", {"form": form})

    # Method to handle post request
    def post(self, request):
        # Initialize the form
        form = LoginForm(request.POST)

        # Check if the form is valid
        if form.is_valid():
            # Get the form data
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")

            # Check if user is active
            user = User.objects.filter(email=email).first()

            # Check if user exists and is not active
            if user and not user.is_active:
                # Add error message
                messages.error(request, "Account Not Activated!", extra_tags="danger")

                # Render the login page
                return render(request, "accounts/login.html", {"form": form})

            # Authenticate the user
            user = authenticate(request, email=email, password=password)

            # Check if the user is authenticated
            if user:
                # Login the user
                login(request, user)

                # Add success message
                messages.success(
                    request, "Logged in Successfully!", extra_tags="success"
                )

                # Redirect to the login page
                return redirect("core:home")

            # Add error message
            messages.error(request, "Invalid Credentials!", extra_tags="danger")

        # Render the login page
        return render(request, "accounts/login.html", {"form": form})


# User Logout View
class LogoutView(View):
    """User Logout View.

    Inherits:
        View

    Methods:
        get: Method to handle get request
    """

    # Method to handle get request
    def get(self, request):
        # Logout the user
        logout(request)

        # Add success message
        messages.success(request, "Logged out Successfully!", extra_tags="success")

        # Redirect to the login page
        return redirect("accounts:login")
