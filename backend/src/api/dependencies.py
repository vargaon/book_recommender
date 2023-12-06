from fastapi import Depends, Request
from typing import Callable, Annotated
from src.models import BaseRepository
from pymongo.database import Database

from src.core.recommender import Recommender


async def get_db(*, request: Request) -> Database:
    return request.app.state.mongo_client["book_recommender"]


def get_repository(repository_type: type[BaseRepository]) -> Callable[..., BaseRepository]:
    def _inner(*, db: Annotated[Database, Depends(get_db)]) -> BaseRepository:
        return repository_type(db)  # type: ignore

    return _inner


async def get_recommender(*, request: Request) -> Recommender:
    pass
