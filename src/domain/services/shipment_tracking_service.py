import hashlib
import time
from typing import Optional

from domain.model.shipment import ShipmentEvent, ShipmentModel
from domain.repositories.shipment_repository import ShipmentRepository
from infrastructure.datastore.repositories.shipment import DatastoreShipmentRepository


class ShipmentTrackingService:
    shipment_repository: ShipmentRepository = DatastoreShipmentRepository()

    def get_shipment(self, shipment_id: str) -> Optional[ShipmentModel]:
        return self.shipment_repository.get_shipment(shipment_id)

    def track_shipment(self, tracking_id: str) -> Optional[ShipmentModel]:
        return self.shipment_repository.get_shipment_by_tracking_id(tracking_id)

    @staticmethod
    def generate_short_hash(data: str, length: int = 11) -> str:
        hash_obj = hashlib.sha1(data.encode())
        return hash_obj.hexdigest()[:length]

    def generate_tracking_id(
        self, receiver, delivery_address: str, user_id: str
    ) -> str:
        timestamp = str(time.time())
        unique_attributes = f"{user_id}{delivery_address}{timestamp}{receiver}"
        short_hash = self.generate_short_hash(unique_attributes)
        return short_hash

    def update_shipment_tracking(
        self, shipment: ShipmentModel, shipment_event: ShipmentEvent
    ):
        shipment.add_event(shipment_event)
        return self.shipment_repository.update_shipment(shipment, shipment_event.status)
