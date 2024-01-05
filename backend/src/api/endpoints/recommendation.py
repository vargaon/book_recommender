from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query

from ..dependencies import get_recommender, Recommender
from ..schemas.recommendation import RecommendationSchema, RecommendationQueryParameters

router = APIRouter()


@router.get(
    "/books2user/{user_id}",
    response_model=RecommendationSchema,
    response_model_exclude_none=True,
)
async def get_books_recommendation_to_user(
    user_id: Annotated[str, Path(title="User identifier")],
    parameters: Annotated[RecommendationQueryParameters, Depends()],
    recommender: Annotated[Recommender, Depends(get_recommender)],
) -> RecommendationSchema:
    """Get recommendation of books to user."""

    return RecommendationSchema.model_validate(
        {
            "recommendation": recommender.recommend_to_user(
                user_id, parameters.count, parameters.iter
            )
        }
    )


@router.get(
    "/books2book/{book_id}",
    response_model=RecommendationSchema,
    response_model_exclude_none=True,
)
async def get_books_recommendation_to_book(
    book_id: Annotated[str, Path(title="Book identifier")],
    parameters: Annotated[RecommendationQueryParameters, Depends()],
    recommender: Annotated[Recommender, Depends(get_recommender)],
) -> RecommendationSchema:
    """Get recommendation of books to book."""

    return RecommendationSchema.model_validate(
        {
            "recommendation": recommender.recommend_to_book(
                book_id, parameters.count, parameters.iter
            )
        }
    )


@router.get(
    "/books2query",
    response_model=RecommendationSchema,
    response_model_exclude_none=True,
)
async def get_books_recommendation_to_query(
    query: Annotated[str, Query(title="Query", max_length=512)],
    parameters: Annotated[RecommendationQueryParameters, Depends()],
    recommender: Annotated[Recommender, Depends(get_recommender)],
) -> RecommendationSchema:
    """Get recommendation of books to given query."""

    return RecommendationSchema.model_validate(
        {
            "recommendation": recommender.recommend_to_query(
                query, parameters.count, parameters.iter
            )
        }
    )
