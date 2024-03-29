from abc import ABC, abstractmethod
from typing import List, Optional

from domain.model.user import UserModel


class UserRepository(ABC):
    @abstractmethod
    def get_user(self, user_id: str) -> Optional[UserModel]:
        raise NotImplementedError

    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[UserModel]:
        raise NotImplementedError

    @abstractmethod
    def create_user(self, user: dict) -> UserModel:
        raise NotImplementedError

    @abstractmethod
    def update_user(self, user: dict) -> UserModel:
        raise NotImplementedError

    @abstractmethod
    def delete_user(self, user_id: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_all_users(self) -> List[UserModel]:
        raise NotImplementedError
