from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import MongoDsn
from pymongo import MongoClient
from chromadb import HttpClient as ChromaCLient
from starlette.middleware.base import BaseHTTPMiddleware

from src.api.middleware import ProcessTimeHeaderMiddleware
from src.api import api

from src.settings import get_settings


def create_app() -> FastAPI:
    """Create FastAPI application

    :return: Application
    :rtype: FastAPI
    """

    settings = get_settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> Any:
        mongo_host = str(
            MongoDsn.build(
                scheme="mongodb",
                username=settings.MONGO_USERNAME,
                password=settings.MONGO_PASSWORD,
                host=settings.MONGO_HOST,
                port=settings.MONGO_PORT,
            )
        )

        app.state.mongo_client = MongoClient(mongo_host)

        app.state.chroma_client = ChromaCLient(
            host=settings.CHROMA_HOST, port=settings.CHROMA_PORT
        )

        yield

        app.state.mongo_client.close()

    app = FastAPI(
        title="Book Recommender API",
        version="0.0.1",
        openapi_url="/api/openapi.json",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins="*",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(BaseHTTPMiddleware, dispatch=ProcessTimeHeaderMiddleware())

    app.include_router(api.router, prefix="/api")

    return app
