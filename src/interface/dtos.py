from pydantic import BaseModel, EmailStr, HttpUrl

from domain.model.base import State
from domain.model.user import Industry


class ShipmentCreateDto(BaseModel):
    user_id: str
    tracking_id: str
    origin_state: str
    origin_address: str
    destination_state: str
    destination_address: str
    receiver: str


class ApiKeyCreateDto(BaseModel):
    name: str
    webhook_url: HttpUrl


class UpdateUserDtO(BaseModel):
    name: str
    email: EmailStr
    organization: str
    industry: Industry
    address: str
    state: State


class CreateUserDtO(UpdateUserDtO):
    password: str


class LoginDto(BaseModel):
    email: EmailStr
    password: str
