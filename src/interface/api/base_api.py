import logging
from typing import Any

from flask import request
from flask_restx import Resource
from pydantic import ValidationError

logger = logging.getLogger(__name__)


class BaseApi(Resource):
    service = None
    serializer = None

    def _validate_payload(self) -> Any:
        """
        Validates the payload of the request.

        This method attempts to validate the payload of the request using the serializer defined in the class. If the payload is valid, it returns the deserialized data. If the payload is invalid, it logs the validation error and raises a `ValidationError` exception.

        Returns:
            Any: The deserialized data if the payload is valid.

        Raises:
            ValidationError: If the payload is invalid.

        """
        try:
            return self.serializer(**request.get_json())
        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            raise e
