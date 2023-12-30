from typing import Annotated

from fastapi import APIRouter, Depends, Path

from src.collections import BooksCollection

from ..dependencies import get_books_collection
from ..schemas.books import BookSchema, BooksSchema, BooksQueryParameters
from ..schemas.http_exceptions import HTTPNotFoundExceptionSchema
from ..errors import HTTPNotFoundError

router = APIRouter()


@router.get(
    "",
    response_model=BooksSchema,
    response_model_exclude_none=True,
)
async def get_books(
    parameters: Annotated[BooksQueryParameters, Depends()],
    collection: Annotated[BooksCollection, Depends(get_books_collection)],
) -> BooksSchema:
    """Get books."""

    return BooksSchema.model_validate(
        {
            "books": collection.get_list(
                title=parameters.title, limit=parameters.limit, offset=parameters.offset
            )
        }
    )


@router.get(
    "/{book_id}",
    response_model=BookSchema,
    response_model_exclude_none=True,
    responses={
        404: {
            "model": HTTPNotFoundExceptionSchema,
            "description": "Book with given identifier not found.",
        }
    },
)
async def get_book_by_id(
    book_id: Annotated[str, Path(title="Book identifier")],
    collection: Annotated[BooksCollection, Depends(get_books_collection)],
) -> BookSchema:
    """Get book by its identifier."""

    if (book := collection.get_by_id(book_id)) is None:
        raise HTTPNotFoundError(f"Book with identifier: {book_id} not found.")

    return BookSchema.model_validate(book)
