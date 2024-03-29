import logging

from flask import abort
from flask_restx import Namespace

from application.services.user_service import UserService
from domain.model.user import UserModel
from interface.api.base_api import AuthenticatedBaseView, BaseView
from interface.dtos import CreateUserDtO, LoginDto, UpdateUserDtO

logger = logging.getLogger(__name__)

api = Namespace("/auth", description="Authentication related operations")


@api.route("/login")
class LoginView(BaseView):
    service = UserService()
    serializer = LoginDto

    def post(self):
        payload: LoginDto = self._validate_payload()
        token = self.service.authenticate(payload.email, payload.password)
        if not token:
            abort(401, "Invalid email or password")

        return {"message": "Login successful", "data": token}


@api.route("/register")
class RegisterView(BaseView):
    serializer = CreateUserDtO
    service = UserService()

    def post(self):
        payload: CreateUserDtO = self._validate_payload()
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


@api.route("/user")
class AccountView(AuthenticatedBaseView):
    serializer = UserModel

    def get(self):
        user: UserModel = self._perform_authentication()
        if not user:
            abort(404, "Account not found")

        return {
            "message": "Account retrieved successfully",
            "data": user.to_serializable_dict(),
        }

    def put(self):
        user: UserModel = self._perform_authentication()
        payload: UpdateUserDtO = self._validate_payload(UpdateUserDtO)
        payload.id = user.id
        user = self.service.update_user(payload)
        if not user:
            abort(404, "Account not found")

        return {
            "message": "Account updated successfully",
            "data": user.to_serializable_dict(),
        }

    def delete(self):
        user: UserModel = self._perform_authentication()
        self.service.delete_user(user.id)
        return {"message": "Account deleted successfully"}
