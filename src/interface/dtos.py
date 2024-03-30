from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, EmailStr, HttpUrl, constr, validator

from domain.model.base import State
from domain.model.shipment import ShipmentStatus
from domain.model.user import Industry


class ShipmentCreateDto(BaseModel):
    user_id: str
    origin_state: State
    origin_address: str
    destination_state: State
    destination_address: str
    receiver: str
    receiver_contact: Optional[EmailStr] = None
    weight_kg: Decimal
    description: Optional[str] = None
    value: Optional[Decimal] = None
    delivery_instructions: Optional[str] = None


class ShipmentEventCreateDto(BaseModel):
    status: ShipmentStatus
    location: str
    notes: Optional[str] = None


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


class ShipmentQueryParam(BaseModel):
    tracking_id: constr(max_length=11, min_length=11, strip_whitespace=True)  # type: ignore
