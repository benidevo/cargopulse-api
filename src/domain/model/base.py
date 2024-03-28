from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel as PydanticBaseModel


class BaseModel(PydanticBaseModel):
    id: UUID = uuid4()
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class State(str, Enum):
    ABUJA = "ABUJA"
    ABIA = "ABIA"
    ADAMAWA = "ADAMAWA"
    AKWA_IBOM = "AKWA IBOM"
    ANAMBRA = "ANAMBRA"
    BAUCHI = "BAUCHI"
    BAYELSA = "BAYELSA"
    BENUE = "BENUE"
    BORNO = "BORNO"
    CROSS_RIVER = "CROSS RIVER"
    DELTA = "DELTA"
    EBONYI = "EBONYI"
    EDO = "EDO"
    EKITI = "EKITI"
    ENUGU = "ENUGU"
    GOMBE = "GOMBE"
    IMO = "IMO"
    JIGAWA = "JIGAWA"
    KADUNA = "KADUNA"
    KANO = "KANO"
    KATSINA = "KATSINA"
    KEBBI = "KEBBI"
    KOGI = "KOGI"
    KWARA = "KWARA"
    LAGOS = "LAGOS"
    NASARAWA = "NASARAWA"
    NIGER = "NIGER"
    OGUN = "OGUN"
    ONDO = "ONDO"
    OSUN = "OSUN"
    OYO = "OYO"
    PLATEAU = "PLATEAU"
    RIVERS = "RIVERS"
    SOKOTO = "SOKOTO"
    TARABA = "TARABA"
    YOBE = "YOBE"
    ZAMFARA = "ZAMFARA"
