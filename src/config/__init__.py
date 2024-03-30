import os

from dotenv import load_dotenv

from .dev import DevConfig
from .prod import ProdConfig

load_dotenv()
env = os.getenv("ENVIRONMENT", "dev")

ConfigMap = {"dev": DevConfig, "prod": ProdConfig}

settings = ConfigMap.get(env)()
