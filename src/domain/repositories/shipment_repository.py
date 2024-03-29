from abc import ABC, abstractmethod
from typing import Optional

from domain.model.shipment import ShipmentModel


class ShipmentRepository(ABC):
    @abstractmethod
    def get_shipment(self, shipment_id: str) -> Optional[ShipmentModel]:
        raise NotImplementedError

    @abstractmethod
    def get_shipment_by_tracking_id(self, tracking_id: str) -> Optional[ShipmentModel]:
        raise NotImplementedError

    @abstractmethod
    def create_shipment(self, shipment: dict) -> ShipmentModel:
        raise NotImplementedError

    @abstractmethod
    def update_shipment(self, shipment: dict) -> ShipmentModel:
        raise NotImplementedError

    @abstractmethod
    def delete_shipment(self, shipment_id: str) -> None:
        raise NotImplementedError
