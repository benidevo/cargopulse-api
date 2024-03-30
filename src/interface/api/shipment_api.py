from flask import abort
from flask_restx import Namespace

from application.services.shipment_service import ShipmentService
from domain.model.shipment import ShipmentModel
from interface.api.base_api import AuthenticatedBaseView, BaseView
from interface.dtos import ShipmentCreateDto, ShipmentEventCreateDto, ShipmentQueryParam
from interface.utils.decorators import authorized_api_call

api = Namespace("/shipments", description="Shipment related operations")


@api.route("/")
class ShipmentView(BaseView):
    serializer = ShipmentCreateDto
    service: ShipmentService = ShipmentService()

    @authorized_api_call
    def post(self):
        self.metrics_service.increment("shipment_api_call")
        payload: ShipmentCreateDto = self._validate_payload()
        shipment = self.service.create_shipment(payload)
        if not shipment:
            abort(500, "Failed to create shipment")

        self.metrics_service.increment("shipment_created")

        return {
            "message": "Shipment created successfully",
            "data": shipment.model_dump(exclude=["user_id"], mode="json"),
        }

    @authorized_api_call
    def get(self):
        self.metrics_service.increment("shipment_api_call")
        query: ShipmentQueryParam = self._validate_query_params(ShipmentQueryParam)
        shipment: ShipmentModel = self.service.get_shipment_by_tracking_id(
            query.tracking_id
        )
        if not shipment:
            abort(404, "Shipment not found")
        return {
            "message": "Shipment retrieved successfully",
            "data": shipment.model_dump(exclude=["user_id"], mode="json"),
        }


@api.route("/<shipment_id>")
class ShipmentDetailView(AuthenticatedBaseView):
    serializer = ShipmentCreateDto
    service: ShipmentService = ShipmentService()

    def get(self, shipment_id: str):
        self._perform_authentication()
        shipment = self.service.get_shipment(shipment_id)
        if not shipment:
            abort(404, "Shipment not found")
        return {
            "message": "Shipment retrieved successfully",
            "data": shipment.to_serializable_dict(),
        }

    def patch(self, shipment_id: str):
        self._perform_authentication()
        payload: ShipmentEventCreateDto = self._validate_payload(ShipmentEventCreateDto)

        shipment = self.service.update_shipment(shipment_id, payload)
        if not shipment:
            self.metrics_service.increment("shipment_update_failed")
            abort(400, "Failed to update shipment")
        self.metrics_service.increment(f"shipment_status_{payload.status}")
        return {
            "message": "Shipment updated successfully",
            "data": shipment.to_serializable_dict(),
        }
