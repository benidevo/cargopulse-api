from typing import Optional

from domain.model.shipment import ShipmentModel
from domain.repositories.shipment_repository import ShipmentRepository
from infrastructure.datastore.repositories.shipment import DatastoreShipmentRepository


class ShipmentTrackingService:
    shipment_repository: ShipmentRepository = DatastoreShipmentRepository()

    def get_shipment(self, shipment_id: str) -> Optional[ShipmentModel]:
        return self.shipment_repository.get_shipment(shipment_id)

    def get_shipment_by_tracking_id(self, tracking_id: str) -> Optional[ShipmentModel]:
        return self.shipment_repository.get_shipment_by_tracking_id(tracking_id)
