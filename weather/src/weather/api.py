import datetime
import uuid
from typing import Awaitable, Callable

import structlog
from fastapi import FastAPI, Query, HTTPException
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from .generator import generate_weather_by_date
from .models import Weather

app = FastAPI()


class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(request_id=request_id)
        response: Response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response


@app.get("/weather", tags=["Weather"])
def get_weather(date: str = Query(description="Date in format YYYY-MM-DD")) -> Weather:
    try:
        datetime.date.fromisoformat(date)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Use format YYYY-MM-DD for date",
        )

    return generate_weather_by_date(date)
