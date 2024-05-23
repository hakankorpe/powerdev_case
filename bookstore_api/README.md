# Bookstore API

A simple FastAPI application for managing books, authors, and genres.

## Features

- List all books, authors, and genres
- Retrieve books by specific authors and genres
- Create new books, authors, and genres
- Update existing books and authors
- Delete books and authors
- List all books of a specific author
- List all books in a specific genre

## API Endpoints

### Books
- **POST /books/**: Add a new book
- **GET /books/{book_id}**: Get details of a specific book
- **PUT /books/{book_id}**: Update details of a specific book
- **DELETE /books/{book_id}**: Delete a specific book
- **GET /books/**: List all books

### Authors
- **POST /authors/**: Add a new author
- **GET /authors/{author_id}**: Get details of a specific author
- **PUT /authors/{author_id}**: Update details of a specific author
- **DELETE /authors/{author_id}**: Delete a specific author
- **GET /authors/**: List all authors
- **GET /authors/{author_id}/books**: List all books of a specific author

### Genres
- **GET /genres/**: List all genres
- **GET /genres/{genre_id}**: Get details of a specific genre
- **GET /genres/{genre_id}/books**: List all books in a specific genre

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/hakankorpe/bookstore_api.git
    cd bookstore_api
    ```

2. Create and activate a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up the database:

    ```bash
    python -c "from app.database import init_db; init_db()"
    ```

## Running the Application

To start the FastAPI application, run:

```bash
uvicorn app.main:app --reload
```

## API Documentation

The interactive API documentation is available at:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Code Coverage

To generate a code coverage report, run:

```bash
coverage run -m pytest
coverage report -m
```

## Running Tests

To run tests, execute `pytest` in the project root directory. Ensure the `test.db` file is deleted before running tests to avoid conflicts.

## Development Environment

This project uses SQLite for the database and FastAPI for the API framework. Ensure you have Python 3.11 or higher installed.

