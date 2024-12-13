# Imports
from django.urls import path

from apps.accounts.views import (
    ActivateView,
    ForgotPasswordView,
    LoginView,
    LogoutView,
    ResetPasswordView,
    SignupView,
)

# Set app name
app_name = "accounts"

# URL Patterns
urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("activate/<uidb64>/<token>/", ActivateView.as_view(), name="activate"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot-password"),
    path(
        "reset-password/<uidb64>/<token>/",
        ResetPasswordView.as_view(),
        name="reset-password",
    ),
]
