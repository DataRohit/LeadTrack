# Imports
import os

import environ
from celery import Celery

# Initialize environment variables
env = environ.Env()

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", env("DJANGO_SETTINGS_MODULE", default="config.settings")
)

# Create a Celery application instance named "leadtrack"
app = Celery("leadtrack")

# Configure Celery to use the settings from the Django settings module
app.config_from_object("django.conf:settings", namespace="CELERY")

# This automatically discovers and loads tasks defined in the Django app modules
app.autodiscover_tasks()
