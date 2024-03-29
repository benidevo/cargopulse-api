from .base import CommonConfig


class DevConfig(CommonConfig):
    FLASK_ENV: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str = "super-secret-key"

    CLOUD_TASKS_URL: str = "http://localhost:5000"
    GCP_PROJECT_ID: str = "cargopulse-dev"
    GCP_LOCATION: str = "us-central1"

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = ""
    REDIS_DB: int = 0

    JWT_ACCESS_TOKEN_EXPIRATION_SECONDS: int = 3600

    DATASTORE_EMULATOR_HOST: str

    PORT: int = 8000
