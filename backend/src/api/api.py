from fastapi import APIRouter

from .endpoints import books, users, recommendation


router = APIRouter()
base_routers: list[tuple[APIRouter, str, str]] = [
    (books.router, "/books", "Books"),
    (users.router, "/users", "Users"),
    (recommendation.router, "/recommendation", "Recommendation"),
]

for r, p, t in base_routers:
    router.include_router(router=r, prefix=p, tags=[t])
