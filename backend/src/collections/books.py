from pymongo.database import Database
from typing import TypedDict


class Book(TypedDict):
    book_id: str
    title: str
    description: str
    image_url: str
    authors: list[str]
    genres: list[str]


class BooksCollection:
    BOOK_ID_COL = "book_id"
    TITLE_COL = "title"
    DESCRIPTION_COL = "description"
    IMAGE_URL_COL = "image_url"
    AUTHORS_COL = "authors"
    GENRES_COL = "genres"

    def __init__(self, db: Database) -> None:
        self._collection = db["books"]

    def get_by_id(self, book_id: str) -> Book | None:
        return self._collection.find_one({"book_id": book_id}, projection={"_id": False})

    def get_list(
        self,
        title: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[Book]:
        filter = {}
        projection = {"_id": False}
        sort = []

        if title is not None:
            filter["$text"] = {"$search": title}
            projection["score"] = {"$meta": "textScore"}
            sort.append(("score", {"$meta": "textScore"}))

        books = self._collection.find(filter=filter, projection={"_id": False})

        if offset is not None:
            books = books.skip(offset)

        if limit is not None:
            books = books.limit(limit)

        return list(books)
