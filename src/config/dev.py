from .base import CommonConfig


class DevConfig(CommonConfig):
    FLASK_ENV: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str

    JWT_ACCESS_TOKEN_EXPIRATION_SECONDS: int
    DATASTORE_EMULATOR_HOST: str
    PORT: int = 8000
