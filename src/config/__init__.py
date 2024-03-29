from dotenv import load_dotenv

from .dev import DevConfig
from .prod import ProdConfig

load_dotenv()

ConfigMap = {"dev": DevConfig, "prod": ProdConfig}

settings = ConfigMap.get("dev")()
