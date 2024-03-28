from flask import Flask
from flask_restx import Api

from config import settings
from interface.api.user_api import api as user_api

app = Flask(__name__)
app.config.from_object(settings)
api = Api(app, version="1.0", title="API Title", description="A simple API")


api.add_namespace(user_api, path="/auth")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
