# ruff: noqa

# Imports
import os
import sys
from pathlib import Path

from django.core.asgi import get_asgi_application

# Get the project base directory
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

# Add the project directory to the system path
sys.path.append(str(BASE_DIR / "apps"))

# Add the django settings module to the environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Initialize the WSGI application
application = get_asgi_application()


# Import websocket application
from config.websocket import websocket_application


# Function to check if request is http or websocket
async def application(scope, receive, send):
    """Function to check if request is http or websocket and call the respective application.

    Args:
        scope (dict): The scope of the request.
        receive (function): The function to receive data.
        send (function): The function to send data.

    Raises:
        NotImplementedError: If the request type is unknown.
    """

    # If the request is a http request
    if scope["type"] == "http":
        # Call the http application
        await application(scope, receive, send)

    # If the request is a websocket request
    elif scope["type"] == "websocket":
        # Call the websocket application
        await websocket_application(scope, receive, send)

    # If the request is of unknown type
    else:
        # Raise an error
        raise NotImplementedError(f"Unknown Scope Type: {scope['type']}")
