from .base import CommonConfig


class ProdConfig(CommonConfig):
    FLASK_ENV: str = "production"
    DEBUG: bool = False
    SECRET_KEY: str

    CLOUD_TASKS_URL: str
    GCP_PROJECT_ID: str
    GCP_LOCATION: str
    GCP_SERVICE_ACCOUNT_EMAIL: str

    REDIS_HOST: str
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str
    REDIS_DB: int = 0

    PORT: int = 80
