from typing import List

from flask import abort
from flask_restx import Namespace

from domain.model.api_key import ApiKeyModel
from domain.services.authentication_service import AuthenticationService
from interface.api.base_api import AuthenticatedBaseView
from interface.dtos import ApiKeyCreateDto

api = Namespace("/api-keys", description="API key related operations")


@api.route("/")
class ApiKeyView(AuthenticatedBaseView):
    serializer = ApiKeyModel
    service = AuthenticationService()

    def post(self):
        user = self._perform_authentication()
        payload: ApiKeyCreateDto = self._validate_payload(ApiKeyCreateDto)
        api_key_model = ApiKeyModel(**payload.model_dump())
        api_key_model.user_id = user.id
        api_key: ApiKeyModel = self.service.create_api_key(api_key_model)
        api_key.webhook_url = str(api_key.webhook_url)
        return {
            "message": "API key created successfully",
            "data": api_key.to_serializable_dict(),
        }

    def get(self):
        user = self._perform_authentication()
        api_keys: List[ApiKeyModel] = self.service.get_user_api_keys(user.id)
        return {
            "message": "API keys retrieved successfully",
            "data": [api_key.to_serializable_dict() for api_key in api_keys],
        }


@api.route("/<api_key_id>")
class ApiKeyDetailView(AuthenticatedBaseView):
    serializer = ApiKeyModel
    service = AuthenticationService()

    def get(self, api_key_id):
        self._perform_authentication()
        api_key: ApiKeyModel = self.service.get_api_key(api_key_id)
        if not api_key:
            abort(404, "API key not found")

        return {
            "message": "API key retrieved successfully",
            "data": api_key.to_serializable_dict(),
        }

    def delete(self, api_key_id):
        self._perform_authentication()
        self.service.delete_api_key(api_key_id)
        return {"message": "API key deleted successfully"}
