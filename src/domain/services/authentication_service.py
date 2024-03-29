import time

import bcrypt
import jwt
from pydantic import EmailStr

from config import settings
from domain.repositories.user_repository import DatastoreUserRepository, UserRepository


class AuthenticationService:
    user_repository: UserRepository = DatastoreUserRepository()

    @classmethod
    def authenticate(cls, email: EmailStr, password: str) -> str:
        user = cls.user_repository.get_user_by_email(email)
        if not user or not cls._compare_passwords(password, user.password):
            return None
        return cls._generate_jwt(user.id)

    @staticmethod
    def _compare_passwords(plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), hashed_password.encode("utf-8")
        )

    @staticmethod
    def hash_password(password: str) -> str:
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        return hashed.decode("utf-8")

    @staticmethod
    def _generate_jwt(user_id: str) -> str:
        access_payload = {
            "user_id": user_id,
            "exp": int(time.time()) + settings.JWT_ACCESS_TOKEN_EXPIRATION_SECONDS,
        }
        access_token = jwt.encode(
            access_payload,
            settings.SECRET_KEY,
            algorithm="HS256",
        )

        return access_token
