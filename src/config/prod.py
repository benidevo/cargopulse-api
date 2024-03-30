from .base import CommonConfig


class ProdConfig(CommonConfig):
    FLASK_ENV: str = "production"
    DEBUG: bool = False
    SECRET_KEY: str

    PORT: int = 80

    PROD_GCP_PROJECT_ID: str
    PROD_GCP_SECRET_NAME: str
