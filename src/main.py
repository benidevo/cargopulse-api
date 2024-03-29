import logging

from flask import Flask, jsonify
from flask_restx import Api

from config import settings
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


@app.errorhandler(Exception)
def handle_unexpected_error(error):
    """Catch unhandled exceptions and return a generic error response."""

    logging.error(f"Unhandled Exception: {error}", exc_info=True)

    response = {"message": "An unexpected error occurred. Please try again later."}
    return jsonify(response), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=settings.PORT)
