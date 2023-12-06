from datetime import datetime
from typing import Annotated, Any

from fastapi import APIRouter, Depends, Path, Query, Response
from starlette.status import HTTP_204_NO_CONTENT

from ..schemas.recommendation import RecommendationSchema, RecommendationQueryParameters
from ..schemas.http_exceptions import HTTPUnauthorizedExceptionSchema

router = APIRouter()


@router.get(
    "/{recommendation_id}",
    response_model=RecommendationSchema,
    response_model_exclude_none=True,
)
async def get_recommendation_by_id(
    recommendation_id: Annotated[str, Path(title="Recommendation identifier")],
) -> RecommendationSchema:
    """Get recommendation by identifier."""
    pass


@router.get(
    "/books2user/{user_id}",
    response_model=RecommendationSchema,
    response_model_exclude_none=True,
)
async def get_books_recommendation_to_user(
    user_id: Annotated[str, Path(title="User identifier")],
    parameters: Annotated[RecommendationQueryParameters, Depends()],
) -> RecommendationSchema:
    """Get recommendation of books to user."""
    pass


@router.get(
    "/books2book/{book_id}",
    response_model=RecommendationSchema,
    response_model_exclude_none=True,
)
async def get_books_recommendation_to_book(
    book_id: Annotated[str, Path(title="Book identifier")],
    parameters: Annotated[RecommendationQueryParameters, Depends()],
) -> RecommendationSchema:
    """Get recommendation of books to book."""
    pass


@router.get(
    "/books2query",
    response_model=RecommendationSchema,
    response_model_exclude_none=True,
)
async def get_books_recommendation_to_query(
    query: Annotated[str, Path(title="Query", max_length=512)],
    parameters: Annotated[RecommendationQueryParameters, Depends()],
) -> RecommendationSchema:
    """Get recommendation of books to given query."""
    pass
