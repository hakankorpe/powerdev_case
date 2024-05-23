from fastapi.testclient import TestClient
from app.main import app
import pytest
from app.dependencies import get_db

client = TestClient(app)

# Override the get_db dependency with the test database
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.mark.usefixtures("setup_database")
def test_create_book():
    response = client.post("/books/", json={
        "title": "Test Book",
        "publication_date": "2024-01-01",
        "author_ids": [1],
        "genre_ids": [1]
    })
    assert response.status_code == 200
    assert response.json()["title"] == "Test Book"

@pytest.mark.usefixtures("setup_database")
def test_read_book():
    response = client.get("/books/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

@pytest.mark.usefixtures("setup_database")
def test_list_genres():
    response = client.get("/genres/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.usefixtures("setup_database")
def test_list_books():
    response = client.get("/books/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.usefixtures("setup_database")
def test_list_authors():
    response = client.get("/authors/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.usefixtures("setup_database")
def test_list_books_by_author():
    response = client.get("/authors/1/books")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.usefixtures("setup_database")
def test_list_books_by_genre():
    response = client.get("/genres/1/books")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
