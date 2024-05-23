# Bookstore API

A simple FastAPI application for managing books, authors, and genres.

## Features

- List all books, authors, and genres
- Retrieve books by specific authors and genres
- Create new books

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/hakankorpe/bookstore_api.git
    cd bookstore_api
    ```

2. Create and activate a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
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

## Running Tests

- To run tests, use:

```bash
pytest
```