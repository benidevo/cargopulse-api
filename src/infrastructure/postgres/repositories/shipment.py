import json
from typing import List, Optional

from domain.model.shipment import ShipmentEvent, ShipmentModel, ShipmentStatus
from domain.repositories.shipment_repository import ShipmentRepository
from infrastructure.postgres.db_objects import Shipment
from src.infrastructure.postgres.client import get_postgres_client


class PostgresShipmentRepository(ShipmentRepository):

    def __init__(self):
        self.session = self._get_session()

    def get_shipment(self, shipment_id: str) -> Optional[ShipmentModel]:
        shipment = self.session.query(Shipment).get(shipment_id)
        if not shipment:
            return None
        return shipment.to_model()

    def get_shipment_by_tracking_id(self, tracking_id: str) -> Optional[ShipmentModel]:
        shipment = (
            self.session.query(Shipment).filter_by(tracking_id=tracking_id).first()
        )
        if not shipment:
            return None
        return shipment.to_model()

    def create_shipment(self, shipment: dict) -> ShipmentModel:
        shipment = Shipment.from_model(shipment)
        self.session.add(shipment)
        self._save()
        return shipment.to_model()

    def update_shipment(
        self, shipment_model: ShipmentModel, shipment_status: ShipmentStatus
    ) -> Optional[ShipmentModel]:
        shipment = self.session.query(Shipment).get(shipment_model.id)
        if not shipment:
            return None

        events: List[ShipmentEvent] = shipment_model.events
        shipment.events = json.dumps([event.model_dump_json() for event in events])
        shipment.status = shipment_status
        self.session.add(shipment)
        self._save()
        return shipment.to_model()

    def get_user_shipments(self, user_id: str) -> Optional[ShipmentModel]:
        shipments = self.session.query(Shipment).filter_by(user_key=user_id).all()

        if not shipments:
            return None
        return [shipment.to_model() for shipment in shipments]

    def _get_session(self):
        return get_postgres_client()

    def _save(self):
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
