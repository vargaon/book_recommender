import time
from typing import Awaitable, Callable

from fastapi import Request, Response


class ProcessTimeHeaderMiddleware:
    """Class to represent middleware for adding process time header"""

    async def __call__(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time

        response.headers["X-Process-Time"] = str(process_time)

        return response
