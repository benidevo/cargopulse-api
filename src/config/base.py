from pydantic_settings import BaseSettings


class CommonConfig(BaseSettings):
    FLASK_APP: str
    JWT_ACCESS_TOKEN_EXPIRATION_SECONDS: int
    ENVIRONMENT: str
    CUMULATIVE_METRIC_START_TIME: str = "2023-01-01T00:00:00Z"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
