from datetime import datetime
from typing import Annotated, Any

from fastapi import APIRouter, Depends, Path, Query, Response
from starlette.status import HTTP_204_NO_CONTENT

from ..schemas.books import (
    UserBookSchema,
    UserBooksSchema,
    UserBookInSchema,
    UserBookUpdateSchema,
    BooksQueryParameters,
)
from ..schemas.http_exceptions import HTTPUnauthorizedExceptionSchema

router = APIRouter()


@router.get(
    "/{user_id}/books",
    response_model=UserBooksSchema,
    response_model_exclude_none=True,
)
async def get_user_books(
    user_id: Annotated[str, Path(title="User identifier")],
    parameters: Annotated[BooksQueryParameters, Depends()],
) -> UserBooksSchema:
    """Get user books."""
    pass


@router.get(
    "/{user_id}/books/{book_id}",
    response_model=UserBookSchema,
    response_model_exclude_none=True,
)
async def get_user_book_by_id(
    user_id: Annotated[str, Path(title="User identifier")],
    book_id: Annotated[str, Path(title="Book identifier")],
) -> UserBookSchema:
    """Get user book by its identifier."""
    pass


@router.post(
    "/{user_id}/books",
    response_model=UserBooksSchema,
    response_model_exclude_none=True,
)
async def create_user_book(
    user_id: Annotated[str, Path(title="User identifier")], data: UserBookInSchema
) -> UserBooksSchema:
    """Create user book."""
    pass


@router.put(
    "/{user_id}/books/{book_id}",
    response_model=UserBooksSchema,
    response_model_exclude_none=True,
)
async def update_user_book(
    user_id: Annotated[str, Path(title="User identifier")],
    book_id: Annotated[str, Path(title="Book identifier")],
    data: UserBookUpdateSchema,
) -> UserBooksSchema:
    """Update user book."""
    pass
