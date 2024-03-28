from pydantic_settings import BaseSettings


class CommonConfig(BaseSettings):
    FLASK_APP: str = "cargopulse"
    JWT_ACCESS_TOKEN_EXPIRATION_SECONDS: int
    ENVIRONMENT: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
