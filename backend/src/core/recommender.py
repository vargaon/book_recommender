from typing import TypedDict

from src.models import Book


class RecommendationRecord(TypedDict):
    book: Book
    score: float


class Recommender:
    def recommend_for_user(self, user: str) -> list[RecommendationRecord]:
        return []

    def recommend_for_book(self, book: Book) -> list[RecommendationRecord]:
        return []

    def recommend_for_query(self, query: str) -> list[RecommendationRecord]:
        return []
