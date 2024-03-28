import json
import logging
from typing import Any, Optional

from infrastructure.redis.redis_client import get_redis_client

logger = logging.getLogger(__name__)


class RedisCacheManager:
    def __init__(self):
        self.client = get_redis_client()

    def set(self, key: str, value: Any, expire: int = None) -> bool:
        """
        Set a value in the cache.

        :param key: Cache key
        :param value: Value to cache
        :param expire: Expiration time in seconds
        :return: True if the operation was successful, False otherwise
        """
        try:
            value = json.dumps(value)
            if expire:
                self.client.setex(key, expire, value)
            else:
                self.client.set(key, value)
            return True
        except Exception as e:
            logger.error(f"Error setting cache for key {key}: {e}")
            return False

    def get(self, key: str) -> Optional[Any]:
        """
        Get a value from the cache.

        :param key: Cache key
        :return: The cached value if available and valid, None otherwise
        """
        try:
            value = self.client.get(key)
            if value is not None:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"Error getting cache for key {key}: {e}")
            return None

    def delete(self, key: str) -> bool:
        """
        Delete a value from the cache.

        :param key: Cache key
        :return: True if a value was deleted, False otherwise
        """
        try:
            return self.client.delete(key) > 0
        except Exception as e:
            logger.error(f"Error deleting cache for key {key}: {e}")
            return False
