import pytest
from fastapi.testclient import TestClient
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, SessionLocal
from app.models import Author, Genre, Book

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_database():
    engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    author = Author(full_name="Test Author", birth_date=date(1970, 1, 1))
    genre = Genre(name="Test Genre")
    book = Book(title="Test Book", publication_date=date(2024, 1, 1))

    db.add(author)
    db.add(genre)
    db.commit()
    
    # Ensure IDs are assigned
    db.refresh(author)
    db.refresh(genre)
    
    # Establish relationships
    book.authors.append(author)
    book.genres.append(genre)
    
    db.add(book)
    db.commit()
    
    db.refresh(book)  # Ensure ID is assigned

    # Print IDs for debugging
    print(f"Author ID: {author.id}")
    print(f"Genre ID: {genre.id}")
    print(f"Book ID: {book.id}")

    yield db
    
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_create_book(setup_database):
    response = client.post("/books/", json={
        "title": "New Book",
        "publication_date": "2024-01-01",
        "author_ids": [1],
        "genre_ids": [1]
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Book"
    assert data["publication_date"] == "2024-01-01"
    assert data["authors"] == [1]
    assert data["genres"] == [1]

def test_list_books(setup_database):
    response = client.get("/books/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["title"] == "Test Book"

def test_list_genres(setup_database):
    response = client.get("/genres/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["name"] == "Test Genre"

def test_list_authors(setup_database):
    response = client.get("/authors/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["full_name"] == "Test Author"

def test_create_book_with_missing_title(setup_database):
    response = client.post("/books/", json={
        "publication_date": "2024-01-01",
        "author_ids": [1],
        "genre_ids": [1]
    })
    assert response.status_code == 422  # Unprocessable Entity

def test_read_non_existent_book(setup_database):
    response = client.get("/books/9999")
    assert response.status_code == 404  # Not Found

def test_create_author(setup_database):
    response = client.post("/authors/", json={
        "full_name": "New Author",
        "birth_date": "1980-01-01"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "New Author"
    assert data["birth_date"] == "1980-01-01"

def test_create_genre(setup_database):
    response = client.post("/genres/", json={
        "name": "New Genre"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "New Genre"

def test_read_author(setup_database):
    response = client.get("/authors/1")
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Test Author"

def test_read_genre(setup_database):
    response = client.get("/genres/1")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Genre"

def test_update_book(setup_database):
    response = client.put("/books/1", json={
        "title": "Updated Book",
        "publication_date": "2024-01-01",
        "author_ids": [1],
        "genre_ids": [1]
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Book"

def test_delete_book(setup_database):
    response = client.delete("/books/1")
    assert response.status_code == 204  # No Content

def test_list_books_by_author(setup_database):
    db = setup_database
    authors = db.query(Author).all()
    books = db.query(Book).all()
    print(f"Authors in DB: {authors}")
    print(f"Books in DB: {books}")
    for book in books:
        print(f"Book {book.id} authors: {book.authors}")

    author = db.query(Author).filter(Author.full_name == "Test Author").first()
    response = client.get(f"/authors/{author.id}/books")
    assert response.status_code == 200
    data = response.json()
    print(f"Books by Author {author.id}: {data}")  # Debugging statement
    assert len(data) > 0

def test_list_books_by_genre(setup_database):
    db = setup_database
    genres = db.query(Genre).all()
    books = db.query(Book).all()
    print(f"Genres in DB: {genres}")
    print(f"Books in DB: {books}")
    for book in books:
        print(f"Book {book.id} genres: {book.genres}")

    genre = db.query(Genre).filter(Genre.name == "Test Genre").first()
    response = client.get(f"/genres/{genre.id}/books")
    assert response.status_code == 200
    data = response.json()
    print(f"Books in Genre {genre.id}: {data}")  # Debugging statement
    assert len(data) > 0

def test_update_author(setup_database):
    response = client.put("/authors/1", json={
        "full_name": "Updated Author",
        "birth_date": "1970-01-01"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Updated Author"
    assert data["birth_date"] == "1970-01-01"

def test_delete_author(setup_database):
    response = client.delete("/authors/1")
    assert response.status_code == 204  # No Content

    # Verify the author was deleted
    response = client.get("/authors/1")
    assert response.status_code == 404  # Not Found
