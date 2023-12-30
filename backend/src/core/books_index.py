from chromadb.api import ClientAPI
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction


class BooksIndex:
    def __init__(self, client: ClientAPI, model_name: str) -> None:
        self._emb_fn = SentenceTransformerEmbeddingFunction(
            model_name=model_name, normalize_embeddings=True
        )
        self._collection = client.get_collection("books", embedding_function=self._emb_fn)

    def get_book_embedding(self, book_id: str) -> list[float] | None:
        result = self._collection.get(book_id, include=["embeddings"])

        if not len(result["embeddings"]) > 0:  # type: ignore
            return None

        return result["embeddings"][0]  # type: ignore

    def get_books_embeddings(self, book_ids: list[str]) -> list[list[float]]:
        result = self._collection.get(book_ids, include=["embeddings"])

        return result["embeddings"]  # type: ignore

    def get_similar_to_book(self, book_id: str, n: int) -> tuple[list[str], list[float]]:
        if (embedding := self.get_book_embedding(book_id)) is None:
            return [], []

        return self.get_similar_to_embedding(embedding, n)  # type: ignore

    def get_similar_to_books(
        self, book_ids: list[str], n: int
    ) -> tuple[list[list[str]], list[list[float]]]:
        embeddings = self.get_books_embeddings(book_ids)

        return self.get_similar_to_embeddings(embeddings, n)

    def get_similar_to_embedding(
        self, embedding: list[float], n: int
    ) -> tuple[list[str], list[float]]:
        result = self._collection.query(query_embeddings=embedding, n_results=n)

        return result["ids"][0][1:], result["distances"][0][1:]  # type: ignore

    def get_similar_to_query(self, query: str, n: int) -> tuple[list[str], list[float]]:
        result = self._collection.query(query_texts=query, n_results=n)

        return result["ids"][0][1:], result["distances"][0][1:]  # type: ignore

    def get_similar_to_embeddings(
        self, embeddings: list[list[float]], n: int
    ) -> tuple[list[list[str]], list[list[float]]]:
        result = self._collection.query(query_embeddings=embeddings, n_results=n)  # type: ignore

        ids = [i[1:] for i in result["ids"]]
        scores = [s[1:] for s in result["distances"]]  # type: ignore

        return ids, scores
