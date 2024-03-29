from flask import abort
from flask_restx import Namespace

from interface.api.base_api import BaseView
from interface.utils.decorators import authorized_api_call

api = Namespace("/shipments", description="Shipment related operations")


@api.route("/")
class ShipmentView(BaseView):
    @authorized_api_call
    def post(self):
        abort(405)
