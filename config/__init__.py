# Import the Celery app instance
from config.celery_app import app as celery_app

# Define the public API of this module to include only the Celery app instance
__all__ = ("celery_app",)
