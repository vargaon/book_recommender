from pymongo.database import Database
from typing import TypedDict

from .base import BaseRepository


class Book(TypedDict):
    book_id: str
    title: str
    description: str
    image_url: str
    authors: list[str]
    genres: list[str]


class BooksRepository(BaseRepository[Book]):
    BOOK_ID_COL = "book_id"
    TITLE_COL = "title"
    DESCRIPTION_COL = "description"
    IMAGE_URL_COL = "image_url"
    AUTHORS_COL = "authors"
    GENRES_COL = "genres"

    def __init__(self, db: Database) -> None:
        super().__init__(db, "books")

    def get_by_id(self, id: str) -> Book | None:
        return self.collection.find_one({"book_id": id}, {"_id": 0})

    def get(
        self, name: str | None = None, limit: int | None = None, offset: int | None = None
    ) -> list[Book]:
        pass

    # def get_list(self, query: dict[str, Any] | None = None) -> list[Book]:
    #     return list(self.collection.find(query))

    # def load(self, ids: str | list[str] | None = None) -> pd.DataFrame:
    #     self._check_before_load()

    #     query: dict[str, Any] = {}

    #     if ids is not None:
    #         if isinstance(ids, str):
    #             query[Items.ITEM_ID_COL] = ids
    #         else:
    #             query[Items.ITEM_ID_COL] = {"$in": ids}

    #     logger.debug(f"Loading items from mongo database")

    #     return find_pandas_all(self.collection, query, projection={"_id": 0})

    # def load_documents(
    #     self, ids: list[str] | None = None, limit: int = 0, offset: int = 0
    # ) -> list[ItemDocument]:
    #     if not self._check_before_load(strict=False):
    #         return []

    #     md_filter: dict[str, Any] = {}

    #     if ids is not None and len(ids) > 0:
    #         md_filter[Items.ITEM_ID_COL] = {"$in": list(ids)}

    #     logger.debug(f"Loading item documents from mongo database")

    #     res = self.collection.find(md_filter, {"_id": 0})

    #     return list(res.skip(offset).limit(limit))

    # def load_document_by_id(self, item_id: str) -> ItemDocument | None:
    #     if not self._check_before_load(strict=False):
    #         return None

    #     logger.debug(f'Loading item document from mongo database by identifier: "{item_id}"')

    #     return self.collection.find_one({Items.ITEM_ID_COL: item_id}, {"_id": 0})

    # def load_documents_by_name(
    #     self, name: str, limit: int = 0, offset: int = 0
    # ) -> list[ItemDocument]:
    #     if not self._check_before_load(strict=False):
    #         return []

    #     logger.debug(f'Loading item documents from mongo database by name: "{name}"')

    #     res = self.collection.find(
    #         {"$text": {"$search": name}}, {"score": {"$meta": "textScore"}, "_id": 0, "score": 0}
    #     )

    #     return list(res.sort([("score", {"$meta": "textScore"})]).skip(offset).limit(limit))

    # def store(self, items: list[ItemDocument] | pd.DataFrame) -> None:
    #     self.collection.drop()

    #     if isinstance(items, pd.DataFrame):
    #         items = items.to_dict("records")  # type: ignore

    #     logger.debug(f"Storing items[{len((items))}] to mongo collection")

    #     self.collection.insert_many(items)

    #     self._create_indexes()

    # def update(self, items: list[ItemDocument] | pd.DataFrame) -> None:
    #     if not self._check:
    #         self.store(items)
    #     else:
    #         if isinstance(items, pd.DataFrame):
    #             item_docs: list[ItemDocument] = items.to_dict("records")  # type: ignore
    #         else:
    #             item_docs = items

    #         for doc in item_docs:
    #             self.update_or_insert_document(doc)

    # def update_or_insert_document(self, item: ItemDocument) -> None:
    #     if not self._check:
    #         self.collection.insert_one(item)

    #     else:
    #         self.collection.replace_one(
    #             filter={Items.ITEM_ID_COL: item["item_id"]},
    #             replacement=item,
    #             upsert=True,
    #         )

    # def _create_indexes(self) -> None:
    #     logger.debug(f"Creating indexes")

    #     self.collection.create_index(Items.ITEM_ID_COL, unique=True)
    #     self.collection.create_index([(Items.NAME_COL, "text")])
