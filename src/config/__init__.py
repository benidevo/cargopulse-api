import os

from config.dev import DevConfig
from config.prod import ProdConfig

ConfigMap = {"dev": DevConfig, "prod": ProdConfig}

settings = ConfigMap.get(os.getenv("environment", "dev"))
