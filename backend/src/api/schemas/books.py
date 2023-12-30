from typing import Annotated
from pydantic import BaseModel, Field, ConfigDict
from fastapi import Query

from .base import BaseQueryParameters


class BookSchema(BaseModel):
    book_id: Annotated[str, Field(title="Book identifier")]
    title: Annotated[str, Field(title="Title")]
    description: Annotated[str, Field(title="Description")]
    image_url: Annotated[str, Field(title="Image url")]
    authors: Annotated[list[str], Field(title="Authors")]
    genres: Annotated[list[str], Field(title="Genres")]

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "book_id": "1",
                "title": "The Hunger Games",
                "description": "WINNING MEANS FAME AND FORTUNE.LOSING MEANS CERTAIN DEATH.THE HUNGER GAMES HAVE BEGUN. . . .In the ruins of a place once known as North America lies the nation of Panem, a shining Capitol surrounded by twelve outlying districts. The Capitol is harsh and cruel and keeps the districts in line by forcing them all to send one boy and once girl between the ages of twelve and eighteen to participate in the annual Hunger Games, a fight to the death on live TV.Sixteen-year-old Katniss Everdeen regards it as a death sentence when she steps forward to take her sister's place in the Games. But Katniss has been close to dead before—and survival, for her, is second nature. Without really meaning to, she becomes a contender. But if she is to win, she will have to start making choices that weight survival against humanity and life against love.",
                "image_url": "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1586722975l/2767052.jpg",
                "authors": ["Suzanne Collins"],
                "genres": [
                    "Young Adult",
                    "Fiction",
                    "Dystopia",
                    "Fantasy",
                    "Science Fiction",
                    "Romance",
                    "Adventure",
                    "Teen",
                    "Post Apocalyptic",
                    "Action",
                ],
            }
        },
    )


class BooksSchema(BaseModel):
    books: Annotated[list[BookSchema], Field(title="Books")]

    model_config = ConfigDict(from_attributes=True)


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
