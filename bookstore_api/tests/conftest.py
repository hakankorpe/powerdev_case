import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, SQLALCHEMY_DATABASE_URL
from app.main import app
from app.models import Author, Genre, Book
from datetime import date

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_database():
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    author1 = Author(full_name="Test Author 1", birth_date=date(1970, 1, 1))
    author2 = Author(full_name="Test Author 2", birth_date=date(1980, 1, 1))
    genre1 = Genre(name="Test Genre 1")
    genre2 = Genre(name="Test Genre 2")
    book1 = Book(title="Test Book 1", publication_date=date(2024, 1, 1), authors=[author1], genres=[genre1])
    book2 = Book(title="Test Book 2", publication_date=date(2025, 2, 2), authors=[author2], genres=[genre2])

    db.add_all([author1, author2, genre1, genre2, book1, book2])
    db.commit()

    yield db

    db.close()
    Base.metadata.drop_all(bind=engine)
