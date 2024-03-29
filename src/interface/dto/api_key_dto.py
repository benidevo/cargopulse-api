from pydantic import BaseModel, HttpUrl


class ApiKeyCreateDto(BaseModel):
    name: str
    webhook_url: HttpUrl
