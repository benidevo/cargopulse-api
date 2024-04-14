import json
import logging
from datetime import datetime
from decimal import Decimal
from typing import List
from uuid import uuid4 as uuid

from pydantic import HttpUrl
from sqlalchemy import UUID, ForeignKey, Numeric, String, func
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from domain.model.api_key import ApiKeyModel
from domain.model.shipment import ShipmentEvent, ShipmentModel
from domain.model.user import UserModel

logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    __abstract__ = True
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid)
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=func.now(), onupdate=func.now()
    )


class User(Base):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(30), nullable=False)
    email: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    organization: Mapped[str] = mapped_column(String(20), nullable=False)
    industry: Mapped[str] = mapped_column(String(20), nullable=False)
    address: Mapped[str] = mapped_column(String(100), nullable=False)
    state: Mapped[str] = mapped_column(String(10), nullable=False)

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, email={self.email}, password={self.password}, organization={self.organization}, industry={self.industry}, address={self.address}, state={self.state})"

    def to_model(self):
        return UserModel(
            id=str(self.id),
            name=self.name,
            email=self.email,
            password=self.password,
            organization=self.organization,
            industry=self.industry,
            address=self.address,
            state=self.state,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @classmethod
    def from_model(cls, model: UserModel):
        return cls(
            id=model.id,
            name=model.name,
            email=model.email,
            password=model.password,
            organization=model.organization,
            industry=model.industry,
            address=model.address,
            state=model.state,
        )


class ApiKey(Base):
    __tablename__ = "api_keys"

    name: Mapped[str] = mapped_column(String(30), nullable=False)
    api_key: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    webhook_url: Mapped[str] = mapped_column(String(200), nullable=False)
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey(User.id), nullable=False, unique=True
    )

    user = relationship("User")

    def __repr__(self):
        return f"ApiKey(name={self.name}, key={self.api_key}, user_id={self.user_id}, webhook_url={self.webhook_url})"

    def to_model(self):
        url = HttpUrl(self.webhook_url)
        return ApiKeyModel(
            id=str(self.id),
            name=self.name,
            key=self.api_key,
            user_id=self.user_id,
            webhook_url=url,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @classmethod
    def from_model(cls, model: ApiKeyModel):
        return cls(
            id=model.id,
            name=model.name,
            api_key=model.key,
            user_id=model.user_id,
            webhook_url=str(model.webhook_url),
        )


class Shipment(Base):
    __tablename__ = "shipments"

    tracking_id: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False)
    origin_state: Mapped[str] = mapped_column(String(30), nullable=False)
    origin_address: Mapped[str] = mapped_column(String(200), nullable=False)
    destination_state: Mapped[str] = mapped_column(String(30), nullable=False)
    destination_address: Mapped[str] = mapped_column(String(200), nullable=False)
    receiver: Mapped[str] = mapped_column(String(30), nullable=False)
    receiver_contact: Mapped[str] = mapped_column(String(30), nullable=False)
    weight_kg: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    description: Mapped[str] = mapped_column(String(200), nullable=False)
    value: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    delivery_instructions: Mapped[str] = mapped_column(String(200), nullable=False)
    events: Mapped[str] = mapped_column(JSON)
    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )
    user = relationship("User")

    def __repr__(self) -> str:
        return f"Shipment(tracking_id={self.tracking_id}, status={self.status}, user_id={self.user_id}, weight_kg={self.weight_kg}, description={self.description}, value={self.value}, receiver={self.receiver}, receiver_contact={self.receiver_contact}, origin_state={self.origin_state}, origin_address={self.origin_address}, destination_state={self.destination_state}, destination_address={self.destination_address})"

    def to_model(self) -> ShipmentModel:
        events = self._deserialize_events()

        return ShipmentModel(
            id=str(self.id),
            user_id=self.user_id,
            tracking_id=self.tracking_id,
            status=self.status,
            origin_state=self.origin_state,
            origin_address=self.origin_address,
            destination_state=self.destination_state,
            destination_address=self.destination_address,
            receiver=self.receiver,
            receiver_contact=self.receiver_contact,
            weight_kg=self.weight_kg,
            description=self.description,
            value=self.value,
            delivery_instructions=self.delivery_instructions,
            events=events,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @classmethod
    def from_model(cls, model: ShipmentModel):
        return cls(
            id=model.id,
            user_id=model.user_id,
            tracking_id=model.tracking_id,
            status=model.status,
            origin_state=model.origin_state,
            origin_address=model.origin_address,
            destination_state=model.destination_state,
            destination_address=model.destination_address,
            receiver=model.receiver,
            receiver_contact=model.receiver_contact,
            weight_kg=model.weight_kg,
            description=model.description,
            value=model.value,
            delivery_instructions=model.delivery_instructions,
        )

    def _deserialize_events(self) -> List[ShipmentEvent] | List:
        events = self.events or []
        if events:
            try:
                events: List[ShipmentEvent] = [
                    ShipmentEvent(**json.loads(event)) for event in events
                ]
                return events
            except json.JSONDecodeError as e:
                logger.error(f"Failed to deserialize shipment events: {e}")
            except Exception as e:
                logger.error(f"Failed to deserialize shipment events: {e}")
        return []
