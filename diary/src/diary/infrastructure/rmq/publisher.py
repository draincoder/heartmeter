import adaptix
from faststream.rabbit.publisher.asyncapi import AsyncAPIPublisher

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

        await self._publisher.publish(payload, self._queue)
