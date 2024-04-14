from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from config import settings


def get_postgres_client():
    engine = create_engine(settings.DATABASE_URL)
    session_factory = sessionmaker(bind=engine)
    return scoped_session(session_factory)
