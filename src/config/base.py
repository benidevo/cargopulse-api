from pydantic import BaseSettings


class CommonConfig(BaseSettings):
    FLASK_APP: str = "cargopulse"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
