from typing import List

from domain.model.api_key import ApiKeyModel
from domain.repositories.api_key_repository import ApiKeyRepository
from domain.services.authentication_service import AuthenticationService
from infrastructure.datastore.repositories.api_key import DatastoreApiKeyRepository


class NotificationService:
    auth_service: AuthenticationService = AuthenticationService
    api_key_repository: ApiKeyRepository = DatastoreApiKeyRepository()

    def create_api_key(self, api_key: ApiKeyModel) -> ApiKeyModel:
        raw_api_key, hashed_api_key = self.auth_service.generate_api_key(
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
