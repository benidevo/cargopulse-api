from typing import List, Optional

from domain.model.api_key import ApiKeyModel
from domain.repositories.api_key_repository import ApiKeyRepository
from domain.repositories.user_repository import UserRepository
from infrastructure.datastore.client import datastore_context
from infrastructure.datastore.db_objects import ApiKey, User
from infrastructure.datastore.repositories.user import DatastoreUserRepository


class DatastoreApiKeyRepository(ApiKeyRepository):
    user_repository: UserRepository = DatastoreUserRepository()

    @datastore_context
    def get_api_key(self, api_key_id: str) -> Optional[ApiKeyModel]:
        api_key = ApiKey.get_by_id(api_key_id)
        if not api_key:
            return None
        return api_key.to_model()

    @datastore_context
    def get_api_key_by_key(self, key: str) -> Optional[ApiKeyModel]:
        api_key = ApiKey.query(ApiKey.key == key).get()
        if not api_key:
            return None
        return api_key.to_model()

    @datastore_context
    def get_api_keys_by_user_id(self, user_id: str) -> List[ApiKeyModel]:
        user = User.get_by_id(user_id)

        api_keys = ApiKey.query(ApiKey.user_key == user.key).fetch()
        if not api_keys:
            return []
        return [api_key.to_model() for api_key in api_keys]

    @datastore_context
    def create_api_key(self, api_key: ApiKeyModel) -> ApiKeyModel:
        api_key = ApiKey.from_model(api_key)
        api_key.put()
        return api_key.to_model()

    @datastore_context
    def delete_api_key(self, api_key_id: str) -> None:
        api_key = ApiKey.get_by_id(api_key_id)
        if not api_key:
            return
        api_key.key.delete()
