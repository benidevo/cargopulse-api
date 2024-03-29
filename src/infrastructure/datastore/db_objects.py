from uuid import uuid4

from google.cloud import ndb
from pydantic import HttpUrl

from domain.model.api_key import ApiKeyModel
from domain.model.shipment import ShipmentModel
from domain.model.user import UserModel


class Base(ndb.Model):
    id = ndb.StringProperty(indexed=True)
    created_at = ndb.DateTimeProperty(auto_now_add=True, indexed=True)
    updated_at = ndb.DateTimeProperty(auto_now=True, indexed=True)

    def __init__(self, *args, **kwargs):
        if not kwargs.get("id"):
            kwargs["id"] = str(uuid4())
            class_name = self.__class__.__name__
            key = ndb.Key(class_name, kwargs["id"])
            kwargs["key"] = key
        super(Base, self).__init__(*args, **kwargs)


class User(Base):
    name = ndb.StringProperty()
    email = ndb.StringProperty(indexed=True)
    password = ndb.StringProperty()
    organization = ndb.StringProperty()
    industry = ndb.StringProperty()
    address = ndb.StringProperty()
    state = ndb.StringProperty()

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, email={self.email}, password={self.password}, organization={self.organization}, industry={self.industry}, address={self.address}, state={self.state})"

    def to_model(self):
        return UserModel(
            id=self.id,
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
    name = ndb.StringProperty()
    api_key = ndb.StringProperty(indexed=True)
    user_key = ndb.KeyProperty(kind=User, indexed=True)
    webhook_url = ndb.StringProperty()

    def __repr__(self):
        return f"ApiKey(name={self.name}, key={self.api_key}, user_id={self.user_key}, webhook_url={self.webhook_url})"

    def to_model(self):
        url = HttpUrl(self.webhook_url)
        return ApiKeyModel(
            id=self.id,
            name=self.name,
            key=self.api_key,
            user_id=self.user_key.id(),
            webhook_url=url,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @classmethod
    def from_model(cls, model: ApiKeyModel):
        user_key = ndb.Key(User, model.user_id)
        return cls(
            id=model.id,
            name=model.name,
            api_key=model.key,
            user_key=user_key,
            webhook_url=str(model.webhook_url),
        )


class Shipment(Base):
    user_key = ndb.KeyProperty(kind=User, indexed=True)
    tracking_id = ndb.StringProperty(indexed=True)
    status = ndb.StringProperty(indexed=True)
    origin_state = ndb.StringProperty()
    origin_address = ndb.StringProperty()
    destination_state = ndb.StringProperty()
    destination_address = ndb.StringProperty()
    receiver = ndb.StringProperty()
    receiver_contact = ndb.StringProperty()
    weight_kg = ndb.StringProperty()
    description = ndb.StringProperty()
    value = ndb.StringProperty()
    delivery_instructions = ndb.StringProperty()
    events = ndb.JsonProperty()

    def __repr__(self) -> str:
        return f"Shipment(tracking_id={self.tracking_id}, status={self.status}, user_id={self.user_id}, weight_kg={self.weight_kg}, description={self.description}, value={self.value}, receiver={self.receiver}, receiver_contact={self.receiver_contact}, origin_state={self.origin_state}, origin_address={self.origin_address}, destination_state={self.destination_state}, destination_address={self.destination_address})"

    def to_model(self) -> ShipmentModel:
        return ShipmentModel(
            id=self.id,
            user_id=self.user_key.id(),
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
            events=self.events,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @classmethod
    def from_model(cls, model: ShipmentModel):
        user_key = ndb.Key(User, model.user_id)
        return cls(
            id=model.id,
            user_key=user_key,
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
            events=model.events,
        )
