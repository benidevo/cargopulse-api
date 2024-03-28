from abc import ABC, abstractmethod
from typing import List, Optional

from domain.model.user import UserModel
from infrastructure.datastore.datastore_client import datastore_context
from infrastructure.datastore.db_objects import User


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


class DatastoreUserRepository(UserRepository):
    @datastore_context
    def get_user(self, user_id: str) -> Optional[UserModel]:
        user = User.get_by_id(user_id)
        if not user:
            return None
        return user.to_model(user)

    @datastore_context
    def get_user_by_email(self, email: str) -> Optional[UserModel]:
        user = User.query(User.email == email).get()
        if not user:
            return None
        return user.to_model(user)

    @datastore_context
    def create_user(self, user: dict) -> UserModel:
        user = User.from_model(user)
        user.put()
        return user.to_model()

    @datastore_context
    def update_user(self, user_model: UserModel) -> Optional[UserModel]:
        user = User.get_by_id(user_model.id)
        if not user:
            return None
        for field, value in user_model.model_dump(exclude_unset=True).items():
            if hasattr(user, field) and value:
                setattr(user, field, value)
        user.put()
        return user.to_model(user)

    @datastore_context
    def delete_user(self, user_id: str) -> None:
        user = User.get_by_id(user_id)
        if not user:
            return
        user.key.delete()

    @datastore_context
    def get_all_users(self) -> List[UserModel]:
        users = User.query().fetch()
        return [user.to_model(user) for user in users]
