import os

from dotenv import load_dotenv

from config.dev import DevConfig
from config.prod import ProdConfig

load_dotenv()

ConfigMap = {"dev": DevConfig, "prod": ProdConfig}

settings = ConfigMap.get("dev")()
