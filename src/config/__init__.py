import os

from dotenv import load_dotenv

from infrastructure.cloud_secrets_client import get_secrets

from .dev import DevConfig
from .prod import ProdConfig

load_dotenv()

env = os.getenv("ENVIRONMENT", "dev")
project_id = os.getenv(f"{env.upper()}_GCP_PROJECT_ID")
secret_name = os.getenv(f"{env.upper()}_GCP_SECRET_NAME")

secrets: dict = get_secrets(project_id=project_id, secret_name=secret_name)

ConfigMap = {"dev": DevConfig, "prod": ProdConfig}

settings = ConfigMap.get(env)(**secrets)
