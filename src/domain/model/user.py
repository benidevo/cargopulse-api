from enum import Enum

from pydantic import EmailStr, SecretStr

from .base import BaseModel, State


class Industry(str, Enum):
    IT = "IT"
    HEALTH = "HEALTH"
    FINANCE = "FINANCE"
    ENTERTAINMENT = "ENTERTAINMENT"
    OTHER = "OTHER"


class UserModel(BaseModel):
    name: str
    email: EmailStr
    password: SecretStr
    organization: str
    industry: Industry
    address: str
    state: State
