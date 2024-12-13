# Imports
from django.urls import path

from apps.accounts.views import ActivateView, LoginView, LogoutView, SignupView

# Set app name
app_name = "accounts"

# URL Patterns
urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("activate/<uidb64>/<token>/", ActivateView.as_view(), name="activate"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
