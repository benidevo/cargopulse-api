from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List, Optional

from pydantic import EmailStr

from .base import BaseModel, State


class ShipmentStatus(str, Enum):
    PENDING = "PENDING"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"
    RETURNED = "RETURNED"


class ShipmentEvent(BaseModel):
    status: ShipmentStatus
    timestamp: datetime
    location: Optional[str] = None
    notes: Optional[str] = None


class ShipmentModel(BaseModel):
    user_id: str
    tracking_id: str
    status: ShipmentStatus = ShipmentStatus.PENDING
    origin_state: State
    origin_address: str
    destination_state: State
    destination_address: str
    receiver: str
    receiver_contact: Optional[EmailStr] = None
    weight_kg: Optional[Decimal] = None
    description: Optional[str] = None
    value: Optional[Decimal] = None
    delivery_instructions: Optional[str] = None
    events: Optional[List[ShipmentEvent]] = []
