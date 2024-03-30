from typing import List, Optional

from domain.model.user import UserModel
from domain.repositories.user_repository import UserRepository
from infrastructure.datastore.client import datastore_context
from infrastructure.datastore.db_objects import User


class DatastoreUserRepository(UserRepository):
    @datastore_context
    def get_user(self, user_id: str) -> Optional[UserModel]:
        user = User.get_by_id(user_id)
        if not user:
            return None
        return user.to_model()

    @datastore_context
    def get_user_by_email(self, email: str) -> Optional[UserModel]:
        user = User.query(User.email == email).get()

        if not user:
            return None
        return user.to_model()

    @datastore_context
    def create_user(self, user: UserModel) -> UserModel:
        user = User.from_model(user)
        user.put()
        return user.to_model()

    @datastore_context
    def update_user(self, user_model: UserModel) -> Optional[UserModel]:
        excluded_fields = {"id", "created_at", "updated_at", "password", "email"}

        user = User.get_by_id(user_model.id)
        if not user:
            return None
        for field, value in user_model.model_dump(
            exclude_unset=True, exclude=excluded_fields
        ).items():
            if hasattr(user, field) and value is not None:
                setattr(user, field, value)
        user.put()
        return user.to_model()

    @datastore_context
    def delete_user(self, user_id: str) -> None:
        user = User.get_by_id(user_id)
        if not user:
            return
        user.key.delete()

    @datastore_context
    def get_all_users(self) -> List[UserModel]:
        users = User.query().fetch()
        return [user.to_model() for user in users]
