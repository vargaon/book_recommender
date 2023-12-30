from fastapi import Depends, Request
from typing import Annotated
from src.collections import RatingsCollection, BooksCollection
from src.core import BooksIndex, Recommender
from pymongo.database import Database
from chromadb.api import ClientAPI

from src.settings import get_settings, Settings


async def _get_mongo_db(*, request: Request) -> Database:
    return request.app.state.mongo_client["book_recommender"]


async def _get_chroma_client(*, request: Request) -> ClientAPI:
    return request.app.state.chroma_client


async def get_ratings_collection(
    *, db: Annotated[Database, Depends(_get_mongo_db)]
) -> RatingsCollection:
    return RatingsCollection(db)


async def get_books_collection(
    *, db: Annotated[Database, Depends(_get_mongo_db)]
) -> BooksCollection:
    return BooksCollection(db)


async def get_books_index(
    *,
    client: Annotated[ClientAPI, Depends(_get_chroma_client)],
    settings: Annotated[Settings, Depends(get_settings)]
) -> BooksIndex:
    return BooksIndex(client, settings.EMBEDDING_MODEL)


async def get_recommender(
    *,
    books_index: Annotated[BooksIndex, Depends(get_books_index)],
    ratings_collection: Annotated[RatingsCollection, Depends(get_ratings_collection)]
) -> Recommender:
    return Recommender(books_index, ratings_collection)
