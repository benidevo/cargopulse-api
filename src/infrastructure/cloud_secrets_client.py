import json
import logging
from functools import lru_cache

from google.cloud import secretmanager


@lru_cache
def get_secrets(secret_name: str, project_id: str) -> dict:
    """
    A function to retrieve secrets from Google Cloud Platform using the specified secret name and project id.

    Parameters:
    - secret_name (str): The name of the secret to retrieve.
    - project_id (str): The id of the project where the secret is stored.

    Returns:
    - dict: A dictionary containing the retrieved secrets.
    """
    if not all([secret_name, project_id]):
        raise ValueError("GCP secret_name and project_id are required to get secrets")
    name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
    try:
        client = secretmanager.SecretManagerServiceClient()
        response = client.access_secret_version(request={"name": name})
        secrets = json.loads(response.payload.data.decode("UTF-8"))
        return secrets
    except Exception as e:
        logging.error(f"Error getting secrets from GCP: {e}")
        raise e
