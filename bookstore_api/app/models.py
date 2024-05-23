# pylint: disable=too-few-public-methods

"""
Database models for the bookstore application.
"""

from sqlalchemy import Column, String, Integer, Date, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# Association tables for many-to-many relationships
book_author_association = Table(
    'book_author', Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id')),
    Column('author_id', Integer, ForeignKey('authors.id'))
)

book_genre_association = Table(
    'book_genre', Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id')),
    Column('genre_id', Integer, ForeignKey('genres.id'))
)

class Book(Base):
    """
    Model for books.
    """
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    publication_date = Column(Date)
    authors = relationship('Author', secondary=book_author_association, back_populates='books')
    genres = relationship('Genre', secondary=book_genre_association, back_populates='books')

class Author(Base):
    """
    Model for authors.
    """
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    birth_date = Column(Date)
    books = relationship('Book', secondary=book_author_association, back_populates='authors')

class Genre(Base):
    """
    Model for genres.
    """
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    books = relationship('Book', secondary=book_genre_association, back_populates='genres')
