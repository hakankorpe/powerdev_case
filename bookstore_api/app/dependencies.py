# pylint: disable=cyclic-import

"""
Dependencies for the bookstore application.
"""

from app.database import SessionLocal

def get_db():
    """
    Dependency to get the database session.
    """
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()
