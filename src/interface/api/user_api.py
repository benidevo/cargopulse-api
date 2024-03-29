import logging

from flask import abort
from flask_restx import Namespace
from pydantic import BaseModel, EmailStr, ValidationError

from application.services.user_service import UserService
from domain.model.user import UserModel
from interface.api.base_api import BaseApi

logger = logging.getLogger(__name__)

api = Namespace("/auth", description="User related operations")


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


@api.route("/login")
class LoginView(BaseApi):
    service = UserService()
    serializer = LoginSchema

    def post(self):
        try:
            payload: LoginSchema = self._validate_payload()
        except ValidationError as e:
            abort(400, f"Validation error: {e}")
        token = self.service.authenticate(payload.email, payload.password)
        if not token:
            abort(401, "Invalid email or password")

        return {"message": "Login successful", "data": token}, 200


@api.route("/register")
class RegisterView(BaseApi):
    serializer = UserModel
    service = UserService()

    def post(self):
        try:
            payload: UserModel = self._validate_payload()
        except ValidationError as e:
            abort(400, f"Validation error: {e}")

        user = self.service.get_user_by_email(payload.email)
        if user:
            abort(409, "User already exists")

        user = self.service.create_user(payload)
        return (
            {
                "message": "User created successfully",
                "data": user.to_serializable_dict(),
            },
            201,
        )
