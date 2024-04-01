from functools import lru_cache, wraps
from typing import Callable

from flask import abort, request

from domain.services.authentication_service import AuthenticationService


@lru_cache
def get_auth_service() -> AuthenticationService:
    return AuthenticationService()


def authorized_api_call(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        api_key = request.headers.get("X-API-KEY")
        identity = request.headers.get("X-IDENTITY")
        if not all([api_key, identity]):
            abort(401, "Invalid credentials")

        auth_service: AuthenticationService = get_auth_service()
        valid_api_key = auth_service.get_api_key(identity)
        if not valid_api_key:
            abort(401, "Invalid credentials")

        if not auth_service.verify_api_key(valid_api_key.key, api_key):
            abort(403, "Permission denied")

        return func(*args, **kwargs)

    return wrapper
