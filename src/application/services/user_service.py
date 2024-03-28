from typing import Optional

from domain.repositories.user_repository import DatastoreUserRepository, UserRepository
from domain.services.authentication_service import AuthenticationService


class UserService:
    user_repository: UserRepository = DatastoreUserRepository()
    auth_service: AuthenticationService = AuthenticationService

    def authenticate(self, email, password) -> Optional[str]:
        return self.auth_service.authenticate(email, password)

    def get_user(self, user_id):
        return self.user_repository.get_user(user_id)

    def get_user_by_email(self, email):
        return self.user_repository.get_user_by_email(email)

    def create_user(self, user):
        return self.user_repository.create_user(user)

    def update_user(self, user):
        return self.user_repository.update_user(user)

    def delete_user(self, user_id):
        return self.user_repository.delete_user(user_id)
