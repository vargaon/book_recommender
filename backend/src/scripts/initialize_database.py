import re
import os
from datetime import datetime

import pandas as pd
from bs4 import BeautifulSoup
from pydantic import MongoDsn

from pymongo import MongoClient
from pymongo.database import Database

import chromadb
from chromadb.api import ClientAPI as ChromaClient
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

from tqdm import tqdm

from src.settings import get_settings

data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
ratings_filename = "ratings.pkl"
books_filename = "books.pkl"


def save_data(dir_path: str, filename: str, data: pd.DataFrame) -> None:
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)

    data.to_pickle(os.path.join(data_dir, filename))


def load_data(dir_path: str, filename: str) -> pd.DataFrame | None:
    file_path = os.path.join(dir_path, filename)
    if os.path.isfile(file_path):
        return pd.read_pickle(file_path)

    return None


def load_ratings() -> pd.DataFrame:
    if (ratings := load_data(data_dir, ratings_filename)) is not None:
        return ratings

    ratings = pd.read_csv(
        "https://github.com/zygmuntz/goodbooks-10k/releases/download/v1.0/ratings.zip",
        compression="zip",
    )
    ratings["timestamp"] = datetime.now()

    ratings["user_id"] = ratings["user_id"].astype(str)
    ratings["book_id"] = ratings["book_id"].astype(str)

    save_data(data_dir, ratings_filename, ratings)

    return ratings


def load_books() -> pd.DataFrame:
    if (books := load_data(data_dir, books_filename)) is not None:
        return books

    books = pd.read_csv(
        "https://github.com/zygmuntz/goodbooks-10k/releases/download/v1.0/books.zip",
        compression="zip",
    )
    bbe = pd.read_csv("https://zenodo.org/record/4265096/files/books_1.Best_Books_Ever.csv")

    def extract_goodreads_book_id(bookId: str) -> int:
        match = re.search(r"\d+", bookId)

        if match is not None:
            return int(match.group())

        return -1

    bbe["goodreads_book_id"] = bbe["bookId"].apply(extract_goodreads_book_id)

    books = pd.merge(books, bbe, how="inner", on="goodreads_book_id")
    not_in_books = bbe[~bbe["goodreads_book_id"].isin(books["goodreads_book_id"].unique())]

    books = books[
        ["book_id", "authors", "original_title", "description", "genres", "coverImg", "image_url"]
    ]
    books = books[~books["original_title"].isna()]
    books = books[~books["description"].isna()]
    mask = (books["coverImg"].isna()) & (~books["image_url"].isna())
    books.loc[mask, "coverImg"] = books.loc[mask, "image_url"]
    books = books[["book_id", "authors", "original_title", "coverImg", "genres", "description"]]
    books = books.rename(columns={"original_title": "title", "coverImg": "image_url"})

    not_in_books = not_in_books[["title", "description", "author", "coverImg", "genres"]]
    not_in_books = not_in_books[~not_in_books["description"].isna()]
    not_in_books = not_in_books.rename(columns={"author": "authors", "coverImg": "image_url"})

    max_book_id = books["book_id"].to_numpy().max()
    not_in_books["book_id"] = list(range(max_book_id + 1, max_book_id + 1 + len(not_in_books)))

    result = pd.concat([books, not_in_books], ignore_index=True)
    result["image_url"] = result["image_url"].fillna("")

    def str_to_list(value: str) -> list[str]:
        value = value.replace("'", "").replace("[", "").replace("]", "")
        return [x.strip() for x in value.split(",")]

    result["authors"] = result["authors"].apply(str_to_list)
    result["description"] = result["description"].apply(
        lambda x: BeautifulSoup(x, features="html.parser").get_text()
    )

    result["genres"] = result["genres"].apply(str_to_list)

    result = result.drop_duplicates(subset=["book_id"], keep="first")

    result["book_id"] = result["book_id"].astype(str)

    save_data(data_dir, books_filename, result)

    return result


def store_ratings(mongo_db: Database, ratings: pd.DataFrame) -> None:
    collection = mongo_db["ratings"]
    collection.drop()

    print(f"Inserting ratings ({len(ratings)}) to mongo database.")
    collection.insert_many(ratings.to_dict("records"))

    print("Creating ratings mongo indexes.")
    collection.create_index([("user_id", 1), ("timestamp", -1)])
    collection.create_index([("book_id", 1), ("timestamp", -1)])
    collection.create_index([("user_id", 1), ("book_id", 1)], unique=True)


def store_books(
    mongo_db: Database,
    books: pd.DataFrame,
) -> None:
    collection = mongo_db["books"]
    collection.drop()

    print(f"Inserting books ({len(books)}) to mongo database")
    collection.insert_many(books.to_dict("records"))

    print(f"Creating books mongo indexes.")
    collection.create_index("book_id", unique=True)
    collection.create_index([("title", "text")])


def store_books_to_index(book_index: chromadb.Collection, books: pd.DataFrame):
    print(f"Inserting books to index.")

    batch_size = 32

    ids = books["book_id"].to_list()
    documents = books["description"].to_list()

    for i in tqdm(range(0, (len(books) // batch_size))):
        from_index = i * batch_size
        to_index = (i + 1) * batch_size

        book_index.add(ids=ids[from_index:to_index], documents=documents[from_index:to_index])


def load_dataset() -> dict[str, pd.DataFrame]:
    print("Loading ratings data")
    ratings = load_ratings()

    print("Loading books data")
    books = load_books()

    print("Filter ratings data by books")
    ratings = ratings[ratings["book_id"].isin(books["book_id"].unique())]

    return {"ratings": ratings, "books": books}


def create_new_book_index(chroma_client: ChromaClient, model_name: str) -> chromadb.Collection:
    try:
        chroma_client.delete_collection("books")
    except:
        pass

    return chroma_client.create_collection(
        "books",
        metadata={"hnsw:space": "ip"},
        embedding_function=SentenceTransformerEmbeddingFunction(
            model_name=model_name, normalize_embeddings=True
        ),
    )


def main() -> None:
    settings = get_settings()

    dataset = load_dataset()

    mongo_client = MongoClient(
        str(
            MongoDsn.build(
                scheme="mongodb",
                username=settings.MONGO_USERNAME,
                password=settings.MONGO_PASSWORD,
                host=settings.MONGO_HOST,
                port=settings.MONGO_PORT,
            )
        )
    )
    mongo_db = mongo_client["book_recommender"]

    # store_ratings(mongo_db, dataset["ratings"])
    store_books(mongo_db, dataset["books"])

    # book_index = create_new_book_index(
    #     chromadb.HttpClient(host=settings.CHROMA_HOST, port=settings.CHROMA_PORT),
    #     settings.EMBEDDING_MODEL,
    # )

    # store_books_to_index(book_index, dataset["books"])


if __name__ == "__main__":
    main()
