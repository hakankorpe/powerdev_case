from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
