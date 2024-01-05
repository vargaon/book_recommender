from typing import TypedDict

from src.collections import RatingsCollection

from .books_index import BooksIndex


class RecommendationRecord(TypedDict):
    book_id: str
    score: float


class Recommender:
    def __init__(self, books_index: BooksIndex, ratings_collection: RatingsCollection) -> None:
        self._books_index = books_index
        self._ratings_collection = ratings_collection

    def recommend_to_user(self, user_id: str, n: int, iter: int) -> list[RecommendationRecord]:
        ratings = self._ratings_collection.get_list(user_id=user_id)

        if not len(ratings) > 0:
            return []

        user_book_ids = [r["book_id"] for r in ratings]

        to_rec = ((iter + 1) * n) + 100

        books_ids, _ = self._books_index.get_similar_to_books(user_book_ids, to_rec)

        candidates: list[tuple[str, int]] = []

        for ids in books_ids:
            candidates += [t for t in zip(ids, list(range(len(ids)))[::-1])]

        res = {}

        for i, s in candidates:
            if i in user_book_ids:
                continue
            if i not in res:
                res[i] = s
            else:
                res[i] += s

        for id in user_book_ids:
            if id in res:
                del res[id]

        from_index = iter * n
        to_index = from_index + n

        res = dict(sorted(res.items(), key=lambda x: -x[1]))

        return self._get_recommendation(
            list(res.keys())[from_index:to_index], list(res.values())[from_index:to_index]
        )

    def recommend_to_book(self, book_id: str, n: int, iter: int) -> list[RecommendationRecord]:
        similar_books = self._books_index.get_similar_to_book(book_id, n, iter)

        return self._get_recommendation(*similar_books)

    def recommend_to_query(self, query: str, n: int, iter: int) -> list[RecommendationRecord]:
        similar_books = self._books_index.get_similar_to_query(query, n, iter)

        return self._get_recommendation(*similar_books)

    def _get_recommendation(
        self, book_ids: list[str], scores: list[float]
    ) -> list[RecommendationRecord]:
        return [
            RecommendationRecord(book_id=book_id, score=score)
            for book_id, score in zip(book_ids, scores)
        ]
