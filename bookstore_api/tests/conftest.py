import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, SQLALCHEMY_DATABASE_URL
from app.models import Author, Genre, Book
from datetime import date

# Create a new database session for testing
@pytest.fixture(scope="module")
def setup_database():
    # Create a new database connection for each test
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Initialize the database session
    db = TestingSessionLocal()
    
    # Add some initial data
    author = Author(full_name="Test Author", birth_date=date(1970, 1, 1))
    genre = Genre(name="Test Genre")
    book = Book(title="Test Book", publication_date=date(2024, 1, 1), authors=[author], genres=[genre])
    db.add(author)
    db.add(genre)
    db.add(book)
    db.commit()
    
    yield db  # this is where the testing happens
    
    # Drop the tables after tests
    Base.metadata.drop_all(bind=engine)
    db.close()
