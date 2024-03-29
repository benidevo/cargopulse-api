from typing import Optional

from google.cloud import ndb

from domain.model.shipment import ShipmentModel
from domain.repositories.shipment_repository import ShipmentRepository
from infrastructure.datastore.datastore_client import datastore_context
from infrastructure.datastore.db_objects import Shipment, User


class DatastoreShipmentRepository(ShipmentRepository):
    @datastore_context
    def get_shipment(self, shipment_id: str) -> Optional[ShipmentModel]:
        shipment = Shipment.get_by_id(shipment_id)
        if not shipment:
            return None
        return shipment.to_model(shipment)

    @datastore_context
    def get_shipment_by_tracking_id(self, tracking_id: str) -> Optional[ShipmentModel]:
        shipment = Shipment.query(Shipment.tracking_id == tracking_id).get()
        if not shipment:
            return None
        return shipment.to_model(shipment)

    @datastore_context
    def create_shipment(self, shipment: dict) -> ShipmentModel:
        shipment = Shipment.from_model(shipment)
        shipment.put()
        return shipment.to_model(shipment)

    @datastore_context
    def update_shipment(self, shipment_model: ShipmentModel) -> Optional[ShipmentModel]:
        shipment = Shipment.get_by_id(shipment_model.id)
        if not shipment:
            return None
        shipment.from_model(shipment_model)
        shipment.put()
        return shipment.to_model(shipment)

    @datastore_context
    def get_user_shipments(self, user_id: str) -> Optional[ShipmentModel]:
        user_key = ndb.Key(User, user_id)
        shipments = Shipment.query(Shipment.user_key == user_key).fetch()
        if not shipments:
            return None
        return [shipment.to_model(shipment) for shipment in shipments]
