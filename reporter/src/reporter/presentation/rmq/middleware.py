import uuid

import structlog
from faststream import BaseMiddleware
from faststream.rabbit.message import RabbitMessage


class RequestIDMiddleware(BaseMiddleware):
    async def on_receive(self) -> None:
        msg: RabbitMessage = self.msg  # type: ignore[assignment]
        request_id = msg.headers.get("request_id") or str(uuid.uuid4())
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(request_id=request_id)
        return await super().on_receive()
