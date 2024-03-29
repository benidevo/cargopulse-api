from functools import lru_cache

from flask import abort, request

from application.services.notification_service import NotificationService
from domain.services.authentication_service import AuthenticationService


@lru_cache
def get_notification_service() -> NotificationService:
    return NotificationService()


def authorized_api_call(func):
    """
    Decorator function that authorizes an API call.

    Parameters:
        func (function): The function to be decorated.

    Returns:
        function: The decorated function.

    Raises:
        401: If the API key or identity is invalid.
    """

    def wrapper(*args, **kwargs):
        api_key = request.headers.get("X-API-KEY")
        identity = request.headers.get("X-IDENTITY")
        if not all([api_key, identity]):
            abort(401, "Invalid API key or identity")

        service: NotificationService = get_notification_service()
        valid_api_key = service.get_api_key(identity)
        if not valid_api_key:
            abort(401, "Invalid API key or identity")

        auth_service: AuthenticationService = AuthenticationService
        if not auth_service.verify_api_key(valid_api_key.key, api_key):
            abort(403, "Permission denied")

        return func(*args, **kwargs)

    return wrapper
