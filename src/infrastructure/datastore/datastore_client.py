import logging
from functools import lru_cache

from google.cloud import ndb

logger = logging.getLogger(__name__)


@lru_cache(maxsize=32)
def get_datastore_client():
    return ndb.Client()


def datastore_context(func):
    def wrapper(*args, **kwargs):
        with get_datastore_client().context():
            logging.info("Datastore operation started")
            try:
                logging.debug(
                    f"Running {func.__name__} with args: {args}, kwargs: {kwargs}"
                )
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Datastore error: {e}")
                raise e

    return wrapper
