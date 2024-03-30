from datetime import datetime
from typing import Optional

from application.interfaces import MetricsService
from domain.model.shipment import ShipmentEvent, ShipmentModel
from domain.repositories.shipment_repository import ShipmentRepository
from domain.services.shipment_tracking_service import ShipmentTrackingService
from infrastructure.cloud_monitoring.metric_service import CloudMetricsService
from infrastructure.datastore.repositories.shipment import DatastoreShipmentRepository
from interface.dtos import ShipmentCreateDto, ShipmentEventCreateDto


class ShipmentService:
    shipment_repository: ShipmentRepository = DatastoreShipmentRepository()
    shipment_tracking_service: ShipmentTrackingService = ShipmentTrackingService()
    metrics_service: MetricsService = CloudMetricsService()

    def get_shipment(self, shipment_id: str) -> Optional[ShipmentModel]:
        return self.shipment_repository.get_shipment(shipment_id)

    def get_shipment_by_tracking_id(self, tracking_id: str) -> Optional[ShipmentModel]:
        return self.shipment_tracking_service.track_shipment(tracking_id)

    def create_shipment(
        self,
        shipment: ShipmentCreateDto,
    ) -> ShipmentModel:
        tracking_id: str = self.shipment_tracking_service.generate_tracking_id(
            shipment.receiver, shipment.destination_address, shipment.user_id
        )
        shipment: ShipmentModel = ShipmentModel(
            **shipment.model_dump(), tracking_id=tracking_id
        )

        return self.shipment_repository.create_shipment(shipment)

    def update_shipment(
        self, shipment_id: str, shipment_event: ShipmentEventCreateDto
    ) -> Optional[ShipmentModel]:
        shipment: Optional[ShipmentModel] = self.get_shipment(shipment_id)
        timestamp = datetime.now()
        shipment_event = ShipmentEvent(
            **shipment_event.model_dump(), timestamp=timestamp
        )
        return self.shipment_tracking_service.update_shipment_tracking(
            shipment, shipment_event
        )

    def get_user_shipments(self, user_id: str) -> Optional[ShipmentModel]:
        return self.shipment_repository.get_user_shipments(user_id)
