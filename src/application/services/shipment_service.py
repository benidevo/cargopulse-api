from typing import Optional

from domain.model.shipment import ShipmentModel
from domain.repositories.shipment_repository import ShipmentRepository
from infrastructure.datastore.repositories.shipment import DatastoreShipmentRepository
from interface.dtos import ShipmentCreateDto


class ShipmentService:
    shipment_repository: ShipmentRepository = DatastoreShipmentRepository()

    def get_shipment(self, shipment_id: str) -> Optional[ShipmentModel]:
        return self.shipment_repository.get_shipment(shipment_id)

    def get_shipment_by_tracking_id(self, tracking_id: str) -> Optional[ShipmentModel]:
        return self.shipment_repository.get_shipment_by_tracking_id(tracking_id)

    def create_shipment(self, shipment: ShipmentCreateDto) -> ShipmentModel:
        return self.shipment_repository.create_shipment(shipment)

    def update_shipment(self, shipment: ShipmentModel) -> ShipmentModel:
        return self.shipment_repository.update_shipment(shipment)

    def get_user_shipments(self, user_id: str) -> Optional[ShipmentModel]:
        return self.shipment_repository.get_user_shipments(user_id)
