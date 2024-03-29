from abc import ABC, abstractmethod
from typing import List, Optional

from domain.model.api_key import ApiKeyModel


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
