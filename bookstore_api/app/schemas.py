# pylint: disable=too-few-public-methods

"""
Schemas for the bookstore application.
"""

from datetime import date
from typing import List
from pydantic import BaseModel, Field, ConfigDict

class BookBase(BaseModel):
    title: str
    publication_date: date

class BookCreate(BookBase):
    author_ids: List[int]
    genre_ids: List[int]

class Book(BookBase):
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
    full_name: str
    birth_date: date

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class GenreBase(BaseModel):
    name: str

class GenreCreate(GenreBase):
    pass

class Genre(GenreBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
