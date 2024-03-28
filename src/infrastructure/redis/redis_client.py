import logging
from functools import lru_cache

from redis import Redis

from config import settings

logger = logging.getLogger(__name__)


@lru_cache
def get_redis_client() -> Redis:
    logger.info("Connecting to Redis")
    try:
        return Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
            db=settings.REDIS_DB,
            decode_responses=True,
        )
    except Exception as e:
        logger.error(f"Error connecting to Redis: {e}")
        raise e
