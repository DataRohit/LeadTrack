# ruff: noqa

# Imports
import os
import sys
from pathlib import Path

from django.core.wsgi import get_wsgi_application

# Get the project base directory
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

# Add the project directory to the system path
sys.path.append(str(BASE_DIR / "apps"))

# Add the django settings module to the environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Initialize the WSGI application
application = get_wsgi_application()
