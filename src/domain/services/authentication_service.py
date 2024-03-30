import hashlib
import hmac
import time
from typing import List

import bcrypt
import jwt
from pydantic import EmailStr, HttpUrl

from config import settings
from domain.model.api_key import ApiKeyModel
from domain.repositories.api_key_repository import ApiKeyRepository
from domain.repositories.user_repository import UserRepository
from infrastructure.datastore.repositories.api_key import DatastoreApiKeyRepository
from infrastructure.datastore.repositories.user import DatastoreUserRepository


class AuthenticationService:
    user_repository: UserRepository = DatastoreUserRepository()
    api_key_repository: ApiKeyRepository = DatastoreApiKeyRepository()

    @classmethod
    def authenticate(cls, email: EmailStr, password: str) -> str:
        user = cls.user_repository.get_user_by_email(email)
        if not user or not cls.compare_passwords(password, user.password):
            return None
        return cls._generate_token(user.id)

    @classmethod
    def compare_passwords(cls, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), hashed_password.encode("utf-8")
        )

    @staticmethod
    def hash_password(password: str) -> str:
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        return hashed.decode("utf-8")

    @staticmethod
    def _generate_token(user_id: str) -> str:
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

    @classmethod
    def verify_token(cls, token: str) -> str | None:
        try:
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            return decoded_token.get("user_id")
        except jwt.exceptions.ExpiredSignatureError:
            return None

    @classmethod
    def generate_api_key(
        cls, webhook_url: HttpUrl, user_id: str, webhook_name: str
    ) -> tuple[str, str]:
        api_key = hmac.new(
            settings.SECRET_KEY.encode("utf-8"),
            str(webhook_url).encode("utf-8")
            + user_id.encode("utf-8")
            + time.ctime().encode("utf-8")
            + webhook_name.encode("utf-8"),
            digestmod=hashlib.sha256,
        ).hexdigest()
        hashed_api_key = bcrypt.hashpw(api_key.encode("utf-8"), bcrypt.gensalt())

        return api_key, hashed_api_key.decode("utf-8")

    @classmethod
    def verify_api_key(cls, hashed_api_key: str, api_key: str) -> bool:
        return bcrypt.checkpw(api_key.encode("utf-8"), hashed_api_key.encode("utf-8"))

    def create_api_key(self, api_key: ApiKeyModel) -> ApiKeyModel:
        raw_api_key, hashed_api_key = self.generate_api_key(
            api_key.webhook_url, api_key.user_id, api_key.name
        )
        api_key.key = hashed_api_key
        api_key = self.api_key_repository.create_api_key(api_key)
        api_key.key = raw_api_key

        return api_key

    def get_user_api_keys(self, user_id: str) -> List[ApiKeyModel]:
        return self.api_key_repository.get_api_keys_by_user_id(user_id)

    def get_api_key(self, api_key_id: str) -> ApiKeyModel:
        return self.api_key_repository.get_api_key(api_key_id)

    def delete_api_key(self, api_key_id: str) -> None:
        self.api_key_repository.delete_api_key(api_key_id)
