from typing import List, Optional

from domain.model.api_key import ApiKeyModel
from domain.repositories.api_key_repository import ApiKeyRepository
from infrastructure.postgres.client import get_postgres_client
from src.infrastructure.postgres.db_objects import ApiKey


class PostgresApiKeyRepository(ApiKeyRepository):
    def __init__(self) -> None:
        self.session = self._get_session()

    def get_api_key(self, api_key_id: str) -> Optional[ApiKeyModel]:
        api_key = self.session.query(ApiKey).get(api_key_id)
        if not api_key:
            return None
        return api_key.to_model()

    def get_api_key_by_key(self, key: str) -> Optional[ApiKeyModel]:
        api_key = self.session.query(ApiKey).filter_by(key=key).first()
        if not api_key:
            return None
        return api_key.to_model()

    def get_api_keys_by_user_id(self, user_id: str) -> List[ApiKeyModel]:
        api_keys = self.session.query(ApiKey).filter_by(user_id=user_id).all()
        if not api_keys:
            return []
        return [api_key.to_model() for api_key in api_keys]

    def create_api_key(self, api_key: ApiKeyModel) -> ApiKeyModel:
        api_key = ApiKey.from_model(api_key)
        self.session.add(api_key)
        self._save()
        return api_key.to_model()

    def delete_api_key(self, api_key_id: str) -> None:
        api_key = self.session.query(ApiKey).get(api_key_id)
        if not api_key:
            return
        self.session.delete(api_key)
        self._save()

    def _get_session(self):
        return get_postgres_client()

    def _save(self):
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
