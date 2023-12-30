from typing import Annotated
from pydantic import BaseModel, Field, ConfigDict
from fastapi import Query

from .base import BaseQueryParameters


class BookRecommendationSchema(BaseModel):
    book_id: Annotated[str, Field(title="Book identifier")]
    score: Annotated[float, Field(title="Recommendation score")]

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={"example": {"book_id": "34", "score": 0.37}},
    )


class RecommendationSchema(BaseModel):
    recommendation: Annotated[list[BookRecommendationSchema], Field(title="Recommendation")]

    model_config = ConfigDict(from_attributes=True)


class RecommendationQueryParameters(BaseQueryParameters):
    """Class to represent recommendation query parameters"""

    def __init__(
        self,
        count: int = Query(10, ge=1, title="Count"),
        offset: int = Query(0, ge=0, title="Offset"),
    ) -> None:
        self.count = count
        self.offset = offset
