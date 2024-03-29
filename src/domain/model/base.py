from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel as PydanticBaseModel


class BaseModel(PydanticBaseModel):
    id: str = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_serializable_dict(self) -> dict:
        """
        Convert the object into a serializable dictionary, excluding specified keys, and converting datetimes to ISO format.
        Returns:
            Dict: The serializable dictionary representation of the object.
        """
        exclude = ("password",)
        model_dict = self.model_dump()
        for key, value in model_dict.items():
            if isinstance(value, datetime):
                model_dict[key] = value.isoformat()

        for key in exclude:
            if key in model_dict:
                del model_dict[key]

        return model_dict


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
