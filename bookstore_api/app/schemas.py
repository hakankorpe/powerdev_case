# pylint: disable=too-few-public-methods

"""
Schemas for the bookstore application.
"""

from datetime import date
from typing import List
from pydantic import BaseModel

class BookBase(BaseModel):
    """Schema for the base book model."""
    title: str
    publication_date: date

class BookCreate(BookBase):
    """Schema for creating a book with author and genre IDs."""
    author_ids: List[int]
    genre_ids: List[int]

class Book(BookBase):
    """Schema for representing a book with nested author and genre IDs."""
    id: int
    authors: List[int]
    genres: List[int]

    class Config:
        """Pydantic configuration to use ORM mode."""
        orm_mode = True

class AuthorBase(BaseModel):
    """Schema for the base author model."""
    full_name: str
    birth_date: date

class AuthorCreate(AuthorBase):
    """Schema for creating an author."""

class Author(AuthorBase):
    """Schema for representing an author."""
    id: int

    class Config:
        """Pydantic configuration to use ORM mode."""
        orm_mode = True

class GenreBase(BaseModel):
    """Schema for the base genre model."""
    name: str

class GenreCreate(GenreBase):
    """Schema for creating a genre."""

class Genre(GenreBase):
    """Schema for representing a genre."""
    id: int

    class Config:
        """Pydantic configuration to use ORM mode."""
        orm_mode = True
