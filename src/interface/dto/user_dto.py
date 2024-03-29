from pydantic import EmailStr

from domain.model.base import BaseModel, State
from domain.model.user import Industry


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
