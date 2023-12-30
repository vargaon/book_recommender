from typing import Annotated
from pydantic import BaseModel, Field, ConfigDict
from fastapi import Query
from datetime import datetime

from .base import BaseQueryParameters


class UserRatingSchema(BaseModel):
    book_id: Annotated[str, Field(title="Book identifier")]
    rating: Annotated[int, Field(title="Rating value", ge=1, le=5)]
    timestamp: Annotated[datetime, Field(title="Rating timestamp")]

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {"book_id": "124", "rating": 3, "timestamp": "2023-12-30T10:30:08.802000"}
        },
    )


class BookRatingSchema(BaseModel):
    user_id: Annotated[str, Field(title="User identifier")]
    rating: Annotated[int, Field(title="Rating value", ge=1, le=5)]
    timestamp: Annotated[datetime, Field(title="Rating timestamp")]

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {"user_id": "1025", "rating": 4, "timestamp": "2023-12-30T10:30:08.802000"}
        },
    )


class UserRatingInSchema(BaseModel):
    book_id: Annotated[str, Field(title="Book identifier")]
    rating: Annotated[int, Field(title="Book rating", ge=1, le=5)]

    model_config = ConfigDict(json_schema_extra={"example": {"book_id": "23", "rating": 5}})


class UserRatingsSchema(BaseModel):
    ratings: Annotated[list[UserRatingSchema], Field(title="Ratings")]

    model_config = ConfigDict(from_attributes=True)


class BookRatingsSchema(BaseModel):
    ratings: Annotated[list[BookRatingSchema], Field(title="Ratings")]

    model_config = ConfigDict(from_attributes=True)


class RatingsQueryParameters(BaseQueryParameters):
    """Class to represent ratings query parameters"""

    def __init__(
        self,
        limit: int = Query(10, ge=1, title="Count"),
        offset: int = Query(0, ge=0, title="Offset"),
    ) -> None:
        self.limit = limit
        self.offset = offset
