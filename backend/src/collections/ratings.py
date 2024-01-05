from pymongo.database import Database
from typing import TypedDict
from datetime import datetime


class Rating(TypedDict):
    user_id: str
    book_id: str
    rating: int
    timestamp: datetime


class RatingsCollection:
    USER_ID_COL = "user_id"
    BOOK_ID_COL = "book_id"
    RATING_COL = "rating"
    TIMESTAMP_COL = "timestamp"

    def __init__(self, db: Database) -> None:
        self._collection = db["ratings"]

    def get_list(
        self,
        user_id: str | None = None,
        book_id: str | None = None,
        ratings: list[int] | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[Rating]:
        filter = {}

        if user_id is not None:
            filter[self.USER_ID_COL] = user_id
        if book_id is not None:
            filter[self.BOOK_ID_COL] = book_id

        if ratings is not None and len(ratings) > 0:
            filter[self.RATING_COL] = {"$in": ratings}

        ratings = self._collection.find(filter=filter, projection={"_id": False})

        if offset is not None:
            ratings = ratings.skip(offset)

        if limit is not None:
            ratings = ratings.limit(limit)

        return list(ratings)

    def insert(self, user_id: str, book_id: str, rating: int, timestamp: datetime) -> Rating:
        document = Rating(user_id=user_id, book_id=book_id, rating=rating, timestamp=timestamp)

        self._collection.replace_one(
            {self.USER_ID_COL: user_id, self.BOOK_ID_COL: book_id}, document, upsert=True
        )

        return document

    def remove(self, user_id: str, book_id: str) -> None:
        self._collection.delete_one({self.USER_ID_COL: user_id, self.BOOK_ID_COL: book_id})
