import logging
from uuid import UUID

from diary.application.interfaces import (
    MeasurementReader,
    ReportPublisher,
    UserReader,
)
from .exceptions import UserNotFoundError

logger = logging.getLogger(__name__)


class RequestReportInteractor:
    def __init__(
        self,
        user_reader: UserReader,
        measurement_reader: MeasurementReader,
        report_publisher: ReportPublisher,
    ) -> None:
        self._user_reader = user_reader
        self._measurement_reader = measurement_reader
        self._report_publisher = report_publisher

    async def request(self, user_id: UUID) -> None:
        user = await self._user_reader.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError(user_id=user_id)

        data = await self._measurement_reader.get_all_by_user_id(user.id)
        await self._report_publisher.publish(user, data)
        logger.info(f"Report for user {user.id} was requested, len={len(data)}")
