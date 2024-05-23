"""
Database configuration for the bookstore application.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def init_db():
    """
    Initialize the database and create tables.
    """
    import app.models  # noqa: F401, pylint: disable=import-outside-toplevel, unused-import
    Base.metadata.create_all(bind=engine)
