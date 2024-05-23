"""
Main module for the FastAPI application.
"""
from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, database

app = FastAPI()

# Initialize the database
database.init_db()

def get_db():
    """
    Dependency to get the database session.
    """
    db_session = database.SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()

@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db_session: Session = Depends(get_db)):
    """
    Create a new book.
    """
    db_book = models.Book(
        title=book.title,
        publication_date=book.publication_date
    )
    db_session.add(db_book)
    db_session.commit()
    db_session.refresh(db_book)

    for author_id in book.author_ids:
        author = db_session.query(models.Author).filter(models.Author.id == author_id).first()
        if author:
            db_book.authors.append(author)

    for genre_id in book.genre_ids:
        genre = db_session.query(models.Genre).filter(models.Genre.id == genre_id).first()
        if genre:
            db_book.genres.append(genre)

    db_session.commit()
    db_session.refresh(db_book)
    return schemas.Book.from_orm(db_book)

@app.get("/books/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db_session: Session = Depends(get_db)):
    """
    Read details of a specific book.
    """
    book = db_session.query(models.Book).filter(models.Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return schemas.Book.from_orm(book)

@app.get("/genres/", response_model=List[schemas.Genre])
def list_genres(db_session: Session = Depends(get_db)):
    """
    List all genres.
    """
    genres = db_session.query(models.Genre).all()
    return [schemas.Genre.from_orm(genre) for genre in genres]

@app.get("/books/", response_model=List[schemas.Book])
def list_books(db_session: Session = Depends(get_db)):
    """
    List all books.
    """
    books = db_session.query(models.Book).all()
    return [schemas.Book.from_orm(book) for book in books]

@app.get("/authors/", response_model=List[schemas.Author])
def list_authors(db_session: Session = Depends(get_db)):
    """
    List all authors.
    """
    authors = db_session.query(models.Author).all()
    return [schemas.Author.from_orm(author) for author in authors]

@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db_session: Session = Depends(get_db)):
    """
    Create a new author.
    """
    db_author = models.Author(
        full_name=author.full_name,
        birth_date=author.birth_date
    )
    db_session.add(db_author)
    db_session.commit()
    db_session.refresh(db_author)
    return schemas.Author.from_orm(db_author)

@app.post("/genres/", response_model=schemas.Genre)
def create_genre(genre: schemas.GenreCreate, db_session: Session = Depends(get_db)):
    """
    Create a new genre.
    """
    db_genre = models.Genre(
        name=genre.name
    )
    db_session.add(db_genre)
    db_session.commit()
    db_session.refresh(db_genre)
    return schemas.Genre.from_orm(db_genre)

@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db_session: Session = Depends(get_db)):
    """
    Read details of a specific author.
    """
    author = db_session.query(models.Author).filter(models.Author.id == author_id).first()
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return schemas.Author.from_orm(author)

@app.get("/genres/{genre_id}", response_model=schemas.Genre)
def read_genre(genre_id: int, db_session: Session = Depends(get_db)):
    """
    Read details of a specific genre.
    """
    genre = db_session.query(models.Genre).filter(models.Genre.id == genre_id).first()
    if genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")
    return schemas.Genre.from_orm(genre)

@app.put("/books/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, book: schemas.BookCreate, db_session: Session = Depends(get_db)):
    """
    Update an existing book.
    """
    db_book = db_session.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    db_book.title = book.title
    db_book.publication_date = book.publication_date

    db_book.authors = []
    for author_id in book.author_ids:
        author = db_session.query(models.Author).filter(models.Author.id == author_id).first()
        if author:
            db_book.authors.append(author)

    db_book.genres = []
    for genre_id in book.genre_ids:
        genre = db_session.query(models.Genre).filter(models.Genre.id == genre_id).first()
        if genre:
            db_book.genres.append(genre)

    db_session.commit()
    db_session.refresh(db_book)
    return schemas.Book.from_orm(db_book)

@app.delete("/books/{book_id}", response_model=None, status_code=204)
def delete_book(book_id: int, db_session: Session = Depends(get_db)):
    """
    Delete a book.
    """
    db_book = db_session.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    db_session.delete(db_book)
    db_session.commit()

@app.get("/authors/{author_id}/books", response_model=List[schemas.Book])
def list_books_by_author(author_id: int, db_session: Session = Depends(get_db)):
    """
    List all books by a specific author.
    """
    author = db_session.query(models.Author).filter(models.Author.id == author_id).first()
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return [schemas.Book.from_orm(book) for book in author.books]

@app.get("/genres/{genre_id}/books", response_model=List[schemas.Book])
def list_books_by_genre(genre_id: int, db_session: Session = Depends(get_db)):
    """
    List all books in a specific genre.
    """
    genre = db_session.query(models.Genre).filter(models.Genre.id == genre_id).first()
    if genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")
    return [schemas.Book.from_orm(book) for book in genre.books]
