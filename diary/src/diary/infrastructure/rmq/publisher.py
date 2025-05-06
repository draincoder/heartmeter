import uuid

import adaptix
from faststream.rabbit.publisher.asyncapi import AsyncAPIPublisher
from structlog.contextvars import get_contextvars

from diary.application.interfaces import ReportPublisher
from diary.domain.models import Measurement, User


class RMQReportPublisher(ReportPublisher):
    def __init__(self, publisher: AsyncAPIPublisher) -> None:
        self._publisher = publisher
        self._queue = "reports"

    async def publish(self, user: User, data: list[Measurement]) -> None:
        raw_user = adaptix.dump(user)
        raw_data = [adaptix.dump(d) for d in data]
        payload = {"user": raw_user, "data": raw_data}
        request_id = get_contextvars().get("request_id") or str(uuid.uuid4())
        headers = {"request_id": request_id}

        await self._publisher.publish(payload, self._queue, headers=headers)
