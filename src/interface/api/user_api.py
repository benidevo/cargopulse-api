import logging

from flask import request
from flask_restx import Namespace, Resource
from pydantic import BaseModel, EmailStr, ValidationError

from application.services.user_service import UserService

api = Namespace("/auth", description="User related operations")
logger = logging.getLogger(__name__)


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


@api.route("/login")
class UserApi(Resource):
    service = UserService()
    serializer = LoginSchema
    validated_data = None

    def post(self):
        try:
            self._validate_payload()
            token = self.service.authenticate(**self.validated_data)
            return {"message": "Login successful", "data": token}, 200
        except ValidationError as e:
            return {"message": "Validation error", "errors": f"{e}"}, 400

    def _validate_payload(self):
        try:
            data = self.serializer(**request.get_json())
            self.validated_data = data.model_dump()
        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            raise e
