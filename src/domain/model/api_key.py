from typing import Optional

from pydantic import HttpUrl

from .base import BaseModel


class ApiKeyModel(BaseModel):
    name: str
    key: str
    user_id: str
    webhook_url: Optional[HttpUrl] = None
