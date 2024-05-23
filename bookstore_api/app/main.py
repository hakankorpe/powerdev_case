"""
Main module for the FastAPI application.
"""

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
    return db_book

@app.get("/books/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db_session: Session = Depends(get_db)):
    """
    Read details of a specific book.
    """
    book = db_session.query(models.Book).filter(models.Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book
