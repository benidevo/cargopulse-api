from typing import Optional, Union

from pydantic import HttpUrl

from .base import BaseModel


class ApiKeyModel(BaseModel):
    name: str
    key: str = None
    user_id: str = None
    webhook_url: Union[HttpUrl, str] = None
