import logging
from typing import List, Optional

from domain.model.user import UserModel
from domain.repositories.user_repository import UserRepository
from infrastructure.postgres.client import get_postgres_client
from infrastructure.postgres.db_objects import User

logger = logging.getLogger(__name__)


class PostgresUserRepository(UserRepository):

    def __init__(self):
        self.session = self._get_session()

    def get_user(self, user_id: str) -> Optional[UserModel]:
        user = self.session.query(User).get(user_id)
        if not user:
            return None
        return user.to_model()

    def get_user_by_email(self, email: str) -> Optional[UserModel]:
        user = self.session.query(User).filter_by(email=email).first()

        if not user:
            return None
        return user.to_model()

    def create_user(self, user: UserModel) -> UserModel:
        user = User.from_model(user)
        self.session.add(user)
        self._save()
        return user.to_model()

    def update_user(self, user_model: UserModel) -> Optional[UserModel]:
        excluded_fields = {"id", "created_at", "updated_at", "password", "email"}

        user = self.session.query(User).get(user_model.id)
        if not user:
            return None
        for field, value in user_model.model_dump(
            exclude_unset=True, exclude=excluded_fields
        ).items():
            if hasattr(user, field) and value is not None:
                setattr(user, field, value)
        self.session.add(user)
        self._save()
        return user.to_model()

    def delete_user(self, user_id: str) -> None:
        user = self.session.query(User).get(user_id)
        if not user:
            return
        self.session.delete(user)
        self._save()

    def get_all_users(self) -> List[UserModel]:
        users = self.session.query(User).all()
        return [user.to_model() for user in users]

    def _get_session(self):
        return get_postgres_client()

    def _save(self):
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            logger.error(f"Failed to save user due to an error: {e}")
