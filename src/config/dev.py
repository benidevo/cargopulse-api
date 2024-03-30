from .base import CommonConfig


class DevConfig(CommonConfig):
    FLASK_ENV: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str

    JWT_ACCESS_TOKEN_EXPIRATION_SECONDS: int
    DATASTORE_EMULATOR_HOST: str
    PORT: int = 8000

    DEV_GCP_PROJECT_ID: str
    DEV_GCP_SECRET_NAME: str
