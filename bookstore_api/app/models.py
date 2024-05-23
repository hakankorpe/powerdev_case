# pylint: disable=too-few-public-methods

"""
Database models for the bookstore application.
"""
from sqlalchemy import Column, Integer, String, Date, Table, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

# Association tables
book_authors = Table(
    'book_authors', Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id')),
    Column('author_id', Integer, ForeignKey('authors.id'))
)

book_genres = Table(
    'book_genres', Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id')),
    Column('genre_id', Integer, ForeignKey('genres.id'))
)

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    publication_date = Column(Date)
    authors = relationship('Author', secondary=book_authors, back_populates='books')
    genres = relationship('Genre', secondary=book_genres, back_populates='books')

class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    birth_date = Column(Date)
    books = relationship('Book', secondary=book_authors, back_populates='authors')

class Genre(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    books = relationship('Book', secondary=book_genres, back_populates='genres')
