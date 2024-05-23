# pylint: disable=too-few-public-methods, arguments-renamed, arguments-differ

"""
Schemas for the bookstore application.
"""

from datetime import date
from typing import List, Optional
from pydantic import BaseModel, ConfigDict

class BookBase(BaseModel):
    """
    Base schema for a book.
    """
    title: str
    publication_date: date

class BookCreate(BookBase):
    """
    Schema for creating a book.
    """
    author_ids: List[int]
    genre_ids: List[int]

class Book(BookBase):
    """
    Schema for a book, including its ID and relationships.
    """
    id: int
    authors: List[int]  # Only return author IDs
    genres: List[int]   # Only return genre IDs

    @classmethod
    def model_validate(cls, model):
        return cls(
            id=model.id,
            title=model.title,
            publication_date=model.publication_date,
            authors=[author.id for author in model.authors],
            genres=[genre.id for genre in model.genres]
        )

    model_config = ConfigDict(from_attributes=True)

class AuthorBase(BaseModel):
    """
    Base schema for an author.
    """
    full_name: str
    birth_date: date

class AuthorCreate(AuthorBase):
    """
    Schema for creating an author.
    """

class Author(AuthorBase):
    """
    Schema for an author, including their ID.
    """
    id: int

    model_config = ConfigDict(from_attributes=True)

class GenreBase(BaseModel):
    """
    Base schema for a genre.
    """
    name: str

class GenreCreate(GenreBase):
    """
    Schema for creating a genre.
    """

class Genre(GenreBase):
    """
    Schema for a genre, including its ID.
    """
    id: int
    subgenres: Optional[List['Genre']] = None

    class Config:
        """
        Configuration class for the Genre Pydantic model.

        Attributes:
            from_attributes (bool): If set to True, 
                allows the Pydantic model to be created from an ORM object using attribute names.
            arbitrary_types_allowed (bool): If set to True, 
                allows Pydantic to validate and serialize arbitrary types.
        """
        from_attributes = True
        arbitrary_types_allowed = True
