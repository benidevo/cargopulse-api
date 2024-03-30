from typing import Optional

from pydantic import EmailStr

from application.interfaces import MetricsService
from domain.model.user import UserModel
from domain.repositories.user_repository import UserRepository
from domain.services.authentication_service import AuthenticationService
from infrastructure.cloud_monitoring.metric_service import CloudMetricsService
from infrastructure.datastore.repositories.user import DatastoreUserRepository


class UserService:
    user_repository: UserRepository = DatastoreUserRepository()
    auth_service: AuthenticationService = AuthenticationService()
    metrics_service: MetricsService = CloudMetricsService()

    def authenticate(self, email, password) -> Optional[str]:
        self.metrics_service.increment("user_login_attempt")
        return self.auth_service.authenticate(email, password)

    def get_user(self, user_id: str) -> Optional[UserModel]:
        return self.user_repository.get_user(user_id)

    def get_user_by_email(self, email: EmailStr) -> Optional[UserModel]:
        return self.user_repository.get_user_by_email(email)

    def create_user(self, user_model: UserModel) -> UserModel:
        hashed_password = self.auth_service.hash_password(user_model.password)
        user_model.password = hashed_password
        self.metrics_service.increment("user_registration")
        return self.user_repository.create_user(user_model)

    def update_user(self, user_model: UserModel) -> UserModel:
        return self.user_repository.update_user(user_model)

    def delete_user(self, user_id: str) -> None:
        self.user_repository.delete_user(user_id)
