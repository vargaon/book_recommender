from typing import Annotated
from pydantic import BaseModel, Field, ConfigDict
from fastapi import Query

from .base import BaseQueryParameters


class BookSchema(BaseModel):
    id: Annotated[str, Field(title="Book identifier")]
    title: Annotated[str, Field(title="Title")]
    description: Annotated[str, Field(title="Description")]
    image_url: Annotated[str, Field(title="Image url")]

    model_config = ConfigDict(from_attributes=True)


class BooksSchema(BaseModel):
    books: Annotated[list[BookSchema], Field(title="Books")]

    model_config = ConfigDict(from_attributes=True)


class UserBookSchema(BaseModel):
    book: Annotated[BookSchema, Field(title="Book")]
    rating: Annotated[int, Field(title="Book rating")]


class UserBookInSchema(BaseModel):
    book_id: Annotated[str, Field(title="Book identifier")]
    rating: Annotated[int, Field(title="Book rating", ge=1, le=5)]


class UserBookUpdateSchema(BaseModel):
    rating: Annotated[int, Field(title="Book rating", ge=1, le=5)]


class UserBooksSchema(BaseModel):
    books: Annotated[list[UserBookSchema], Field(title="Books")]


class BooksQueryParameters(BaseQueryParameters):
    """Class to represent books query parameters"""

    def __init__(
        self,
        title: str
        | None = Query(
            None,
            title="Book title",
            description="The title by which books with the most similar title are searched.",
        ),
        limit: int = Query(10, ge=1, title="Limit"),
        offset: int = Query(0, ge=0, title="Offset"),
    ) -> None:
        self.title = title
        self.limit = limit
        self.offset = offset
