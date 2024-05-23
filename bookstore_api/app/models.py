# pylint: disable=too-few-public-methods

"""
Models for the bookstore application.
"""
from sqlalchemy import Column, Integer, String, Date, Table, ForeignKey
from sqlalchemy.orm import relationship, backref
from app.database import Base

# Association tables for many-to-many relationships
book_authors = Table(
    'book_authors', Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id'), primary_key=True),
    Column('author_id', Integer, ForeignKey('authors.id'), primary_key=True)
)

book_genres = Table(
    'book_genres', Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id'), primary_key=True),
    Column('genre_id', Integer, ForeignKey('genres.id'), primary_key=True)
)

class Book(Base):
    """
    Book model representing the books in the bookstore.
    """
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    publication_date = Column(Date)
    authors = relationship('Author', secondary=book_authors, back_populates='books')
    genres = relationship('Genre', secondary=book_genres, back_populates='books')

class Author(Base):
    """
    Author model representing the authors of books in the bookstore.
    """
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    birth_date = Column(Date)
    books = relationship('Book', secondary=book_authors, back_populates='authors')

class Genre(Base):
    """
    Genre model representing the genres of books in the bookstore.
    """
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    parent_id = Column(Integer, ForeignKey('genres.id'), nullable=True)
    parent = relationship(
        'Genre',
        remote_side=[id],
        backref=backref('subgenres', remote_side=[parent_id]))
    books = relationship("Book", secondary=book_genres, back_populates="genres")
