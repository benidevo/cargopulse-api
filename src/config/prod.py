from .base import CommonConfig


class ProdConfig(CommonConfig):
    FLASK_ENV: str = "production"
    DEBUG: bool = False
    SECRET_KEY: str

    GCP_SERVICE_ACCOUNT_EMAIL: str

    PORT: int = 80
