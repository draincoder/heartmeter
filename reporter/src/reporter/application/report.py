import logging
from datetime import date

from reporter.application.dto import History, Weather
from reporter.application.interfaces import ReportGenerator, ReportSender, WeatherReader
from reporter.domain.models import Measurement

logger = logging.getLogger(__name__)


class ReportInteractor:
    def __init__(self, generator: ReportGenerator, sender: ReportSender, weather: WeatherReader) -> None:
        self._generator = generator
        self._sender = sender
        self._weather = weather

    async def report(self, data: History) -> None:
        weathers = await self._get_weathers(data.data)
        report = self._generator.generate(data.data, weathers)
        logger.info("Report generated", extra={"user_id": data.user.id, "report_filename": report.filename})
        await self._sender.send(data.user, report)
        logger.info(
            "Report successfully sent",
            extra={"user_id": data.user.id, "email": data.user.email, "report_filename": report.filename},
        )

    async def _get_weathers(self, data: list[Measurement]) -> dict[date, Weather]:
        weathers: dict[date, Weather] = {}

        for m in data:
            d = m.date.date()
            if d in weathers:
                continue
            weathers[d] = await self._weather.get(d)

        return weathers
