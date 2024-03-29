import logging
from typing import Any, Optional

from flask import abort, request
from flask_restx import Resource
from pydantic import ValidationError

from application.services.user_service import UserService
from domain.model.user import UserModel
from domain.services.authentication_service import AuthenticationService

logger = logging.getLogger(__name__)


class BaseView(Resource):
    service = None
    serializer = None

    def _validate_payload(self, _serializer=None) -> Any:
        """
        Validates the payload of the request.

        This method attempts to validate the payload of the request using the serializer defined in the class. If the payload is valid, it returns the deserialized data. If the payload is invalid, it logs the validation error and raises a `ValidationError` exception.

        Returns:
            Any: The deserialized data if the payload is valid.

        Raises:
            ValidationError: If the payload is invalid.

        """
        if not _serializer:
            _serializer = self.serializer
        try:
            return _serializer(**request.get_json())
        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            abort(400, f"Validation error: {e.errors()}")


class AuthenticatedBaseView(BaseView):
    auth_service = AuthenticationService
    service = UserService()

    @staticmethod
    def _extract_authorization_token() -> str:
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None
        try:
            _, token = auth_header.split(" ")
        except ValueError:
            return None
        return token

    def _perform_authentication(self) -> Optional[UserModel]:
        """
        Perform authentication for the user based on the provided authorization token.

        Returns:
            Optional[UserModel]: The authenticated user if successful, None otherwise.
        """
        token = self._extract_authorization_token()
        if not token:
            abort(401, "Missing or invalid authorization token")
        user_id = self.auth_service.verify_token(token)
        if not user_id:
            abort(401, "Invalid or expired token")

        user = self.service.get_user(user_id)
        if not user:
            abort(401, "Invalid or expired token")

        return user
