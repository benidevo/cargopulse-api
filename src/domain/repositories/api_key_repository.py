from abc import ABC, abstractmethod
from typing import List, Optional

from domain.model.api_key import ApiKeyModel
from infrastructure.datastore.datastore_client import datastore_context
from infrastructure.datastore.db_objects import ApiKey


class ApiKeyRepository(ABC):
    @abstractmethod
    def get_api_key(self, api_key_id: str) -> Optional[ApiKeyModel]:
        raise NotImplementedError

    @abstractmethod
    def get_api_key_by_key(self, key: str) -> Optional[ApiKeyModel]:
        raise NotImplementedError

    @abstractmethod
    def get_api_keys_by_user_id(self, user_id: str) -> List[ApiKeyModel]:
        raise NotImplementedError

    @abstractmethod
    def create_api_key(self, api_key: dict) -> ApiKeyModel:
        raise NotImplementedError

    @abstractmethod
    def update_webhook_url(
        self, user_id: str, api_key_id: str, webhook_url: str
    ) -> Optional[ApiKeyModel]:
        raise NotImplementedError

    @abstractmethod
    def delete_api_key(self, api_key_id: str) -> None:
        raise NotImplementedError


class DatastoreApiKeyRepository(ApiKeyRepository):
    @datastore_context
    def get_api_key(self, api_key_id: str) -> Optional[ApiKeyModel]:
        api_key = ApiKey.get_by_id(api_key_id)
        if not api_key:
            return None
        return api_key.to_model(api_key)

    @datastore_context
    def get_api_key_by_key(self, key: str) -> Optional[ApiKeyModel]:
        api_key = ApiKey.query(ApiKey.key == key).get()
        if not api_key:
            return None
        return api_key.to_model(api_key)

    @datastore_context
    def get_api_keys_by_user_id(self, user_id: str) -> List[ApiKeyModel]:
        api_keys = ApiKey.query(ApiKey.user_id == user_id).fetch()
        if not api_keys:
            return []
        return [api_key.to_model(api_key) for api_key in api_keys]

    @datastore_context
    def create_api_key(self, api_key: dict) -> ApiKeyModel:
        api_key = ApiKey.from_model(api_key)
        api_key.put()
        return api_key.to_model(api_key)

    @datastore_context
    def update_webhook_url(
        self, user_id: str, api_key_id: str, webhook_url: str
    ) -> Optional[ApiKeyModel]:
        api_key = ApiKey.query(ApiKey.user_id == user_id, ApiKey.id == api_key_id).get()
        if not api_key:
            return None
        api_key.webhook_url = webhook_url
        api_key.put()
        return api_key.to_model(api_key)

    @datastore_context
    def delete_api_key(self, api_key_id: str) -> None:
        api_key = ApiKey.get_by_id(api_key_id)
        if not api_key:
            return
        api_key.key.delete()
