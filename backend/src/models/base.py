from typing import TypeVar, Generic, Any
from pymongo.database import Database
from pymongo.collection import Collection

from abc import ABC

T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    def __init__(self, db: Database, collection: str) -> None:
        self._db = db
        self._collection = collection

    @property
    def collection(self) -> Collection:
        """Get collection

        :return: Collection
        :rtype: Collection
        """

        return self._db[self._collection]

    def get_list(
        self,
        filter: dict[str, Any] | None = None,
        projection: dict[str, Any] | None = None,
        sort: list[tuple[str, Any]] | None = None,
        limit: int | None = None,
        skip: int | None = None,
    ) -> list[T]:
        """_summary_

        :param filter: _description_, defaults to None
        :type filter: dict[str, Any] | None, optional
        :param projection: _description_, defaults to None
        :type projection: dict[str, Any] | None, optional
        :param sort: _description_, defaults to None
        :type sort: list[tuple[str, any]] | None, optional
        :param limit: _description_, defaults to None
        :type limit: int | None, optional
        :param skip: _description_, defaults to None
        :type skip: int | None, optional
        :return: _description_
        :rtype: list[T]
        """

        if projection and "_id" not in projection:
            projection["_id"] = False

        return list(
            self.collection.find(
                filter=filter, projection=projection, sort=sort, limit=limit, skip=skip
            )
        )

    def save(self, data: T) -> None:
        """_summary_

        :param data: _description_
        :type data: T
        """

        self.collection.insert_one(data)

    def save_many(self, data: list[T]) -> None:
        """_summary_

        :param data: _description_
        :type data: list[T]
        """

        self.collection.insert_many(data)
