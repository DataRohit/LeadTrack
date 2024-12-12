# Imports
from django.http import HttpResponseForbidden


# Decorator to check if user is authenticated
def role_required(allowed_roles: list[str]):
    """Role Required

    Decorator to check if user is authenticated and has a valid role.

    Args:
        allowed_roles (list[str]): The list of allowed roles.

    Returns:
        function: The decorator function.

    Raises:
        HttpResponseForbidden: If user is not authenticated or does not have a valid role.
    """

    # Decorator function
    def decorator(view_func):
        # Wrapper function
        def _wrapped_view(request, *args, **kwargs):
            # If user is authenticated and has a valid role
            if request.user.is_authenticated and request.user.role in allowed_roles:
                # Call the view function
                return view_func(request, *args, **kwargs)

            # If user is not authenticated or does not have a valid role
            return HttpResponseForbidden(
                "You do not have permission to access this page."
            )

        # Return the wrapper function
        return _wrapped_view

    # Return the decorator function
    return decorator
