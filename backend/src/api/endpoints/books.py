from datetime import datetime
from typing import Annotated, Any

from fastapi import APIRouter, Depends, Path, Query, Response
from starlette.status import HTTP_204_NO_CONTENT

from src.models import BooksRepository

from ..dependencies import get_repository

from ..schemas.books import BookSchema, BooksSchema, BooksQueryParameters
from ..schemas.http_exceptions import HTTPUnauthorizedExceptionSchema

router = APIRouter()


@router.get(
    "",
    response_model=BooksSchema,
    response_model_exclude_none=True,
)
async def get_books(
    parameters: Annotated[BooksQueryParameters, Depends()],
    books: BooksRepository = Depends(get_repository(BooksRepository)),
) -> BooksSchema:
    """Get books."""

    return BooksSchema.model_validate(
        books.get_list(limit=parameters.limit, skip=parameters.offset)
    )


@router.get(
    "{book_id}",
    response_model=BookSchema,
    response_model_exclude_none=True,
)
async def get_book_by_id(
    book_id: Annotated[str, Path(title="Book identifier")],
    books: BooksRepository = Depends(get_repository(BooksRepository)),
) -> BookSchema:
    """Get book by its identifier."""

    if (res := books.get_by_id(book_id)) is None:
        pass

    return BookSchema.model_validate(res)
