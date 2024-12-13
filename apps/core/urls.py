# Imports
from django.urls import path
from django.views.generic import TemplateView

# Set app name
app_name = "core"

# URL Patterns
urlpatterns = [
    path("", TemplateView.as_view(template_name="core/home.html"), name="home"),
]
