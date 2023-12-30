from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Path, status

from src.collections import RatingsCollection

from ..dependencies import get_ratings_collection

from ..schemas.ratings import (
    UserRatingSchema,
    UserRatingsSchema,
    BookRatingsSchema,
    RatingsQueryParameters,
    UserRatingInSchema,
)
from ..schemas.http_exceptions import HTTPNotFoundExceptionSchema
from ..errors import HTTPNotFoundError

router = APIRouter()


@router.get(
    "/user/{user_id}",
    response_model=UserRatingsSchema,
    response_model_exclude_none=True,
)
async def get_user_ratings(
    user_id: Annotated[str, Path(title="User identifier")],
    parameters: Annotated[RatingsQueryParameters, Depends()],
    collection: Annotated[RatingsCollection, Depends(get_ratings_collection)],
) -> UserRatingsSchema:
    """Get user ratings."""

    return UserRatingsSchema.model_validate(
        {"ratings": collection.get_list(user_id, limit=parameters.limit, offset=parameters.offset)}
    )


@router.post(
    "/user/{user_id}",
    response_model=UserRatingSchema,
    response_model_exclude_none=True,
)
async def create_user_rating(
    user_id: Annotated[str, Path(title="User identifier")],
    data: UserRatingInSchema,
    collection: Annotated[RatingsCollection, Depends(get_ratings_collection)],
) -> UserRatingSchema:
    """Create user rating of book."""

    return UserRatingSchema.model_validate(
        collection.insert(user_id, data.book_id, data.rating, datetime.now())
    )


@router.get(
    "/user/{user_id}/book/{book_id}",
    response_model=UserRatingSchema,
    response_model_exclude_none=True,
    responses={
        404: {
            "model": HTTPNotFoundExceptionSchema,
            "description": "User rating of book with given identifier not found.",
        }
    },
)
async def get_user_rating_of_book(
    user_id: Annotated[str, Path(title="User identifier")],
    book_id: Annotated[str, Path(title="Book identifier")],
    collection: Annotated[RatingsCollection, Depends(get_ratings_collection)],
) -> UserRatingSchema:
    """Get user rating of book."""

    ratings = collection.get_list(user_id, book_id)

    if not len(ratings) > 0:
        raise HTTPNotFoundError(f"User rating of book with identifier: {book_id} not found.")

    return UserRatingSchema.model_validate(ratings[0])


@router.delete("/user/{user_id}/book/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_rating_of_book(
    user_id: Annotated[str, Path(title="User identifier")],
    book_id: Annotated[str, Path(title="Book identifier")],
    collection: Annotated[RatingsCollection, Depends(get_ratings_collection)],
) -> None:
    """Delete user rating of book."""

    collection.remove(user_id, book_id)


@router.get(
    "/book/{book_id}",
    response_model=BookRatingsSchema,
    response_model_exclude_none=True,
)
async def get_book_ratings(
    book_id: Annotated[str, Path(title="Book identifier")],
    parameters: Annotated[RatingsQueryParameters, Depends()],
    collection: Annotated[RatingsCollection, Depends(get_ratings_collection)],
) -> BookRatingsSchema:
    """Get book ratings."""

    return BookRatingsSchema.model_validate(
        {
            "ratings": collection.get_list(
                book_id=book_id, limit=parameters.limit, offset=parameters.offset
            )
        }
    )
