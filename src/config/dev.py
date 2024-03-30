from .base import CommonConfig


class DevConfig(CommonConfig):
    FLASK_ENV: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str = "super-secret-key"

    JWT_ACCESS_TOKEN_EXPIRATION_SECONDS: int = 3600
    DATASTORE_EMULATOR_HOST: str
    PORT: int = 8000
