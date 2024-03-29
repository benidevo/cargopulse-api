from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel as PydanticBaseModel


class BaseModel(PydanticBaseModel):
    id: str = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_serializable_dict(self) -> dict:
        """
        Return a serializable dictionary representation of the model, excluding the 'password' field.
        The dictionary will contain the model's data, with any datetime values converted to ISO format and any values containing 'url' converted to strings.
        Returns:
            dict: The serializable dictionary representation of the model.
        """
        exclude = ("password",)
        model_dict = self.model_dump(exclude=exclude)
        for key, value in model_dict.items():
            if isinstance(value, datetime):
                model_dict[key] = value.isoformat()
            if "url" in key:
                model_dict[key] = str(value)

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
