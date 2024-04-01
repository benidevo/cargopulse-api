import logging

from flask import Flask, jsonify
from flask_restx import Api
from werkzeug.exceptions import NotFound

from config import settings
from interface.api.api_key_api import api as api_key_api
from interface.api.shipment_api import api as shipment_api
from interface.api.user_api import api as user_api

app = Flask(__name__)
app.config.from_object(settings)
api = Api(
    app,
    version="1.0",
    title="CargoPulse API",
    description="A simple API for managing logistics-related tasks such as shipment tracking and user management.",
)


api.add_namespace(user_api, path="/auth")
api.add_namespace(api_key_api, path="/api-keys")
api.add_namespace(shipment_api, path="/shipments")


@app.errorhandler(Exception)
def handle_unexpected_error(error):
    """Catch unhandled exceptions and return a generic error response."""

    logging.error(f"Unhandled Exception: {error}", exc_info=True)

    if isinstance(error, NotFound):
        return jsonify({"message": str(error)}), 404

    response = {"message": "An unexpected error occurred. Please try again later."}
    return jsonify(response), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=settings.PORT)
