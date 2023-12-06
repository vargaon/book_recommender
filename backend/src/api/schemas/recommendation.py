from typing import Annotated
from pydantic import BaseModel, Field
from fastapi import Query

from .books import BookSchema
from .base import BaseQueryParameters


class BookRecommendationSchema(BaseModel):
    item: Annotated[BookSchema, Field(title="Item")]
    score: Annotated[float, Field(title="Recommendation score")]


class RecommendationSchema(BaseModel):
    recommendation: Annotated[list[BookRecommendationSchema], Field(title="Recommendation")]


class RecommendationQueryParameters(BaseQueryParameters):
    """Class to represent recommendation query parameters"""

    def __init__(
        self,
        count: int = Query(10, ge=1, title="Count"),
        offset: int = Query(0, ge=0, title="Offset"),
    ) -> None:
        self.count = count
        self.offset = offset
