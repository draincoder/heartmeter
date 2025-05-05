from datetime import date

from reporter.application.dto import History, Weather
from reporter.application.interfaces import ReportGenerator, ReportSender, WeatherReader
from reporter.domain.models import Measurement


class ReportInteractor:
    def __init__(self, generator: ReportGenerator, sender: ReportSender, weather: WeatherReader) -> None:
        self._generator = generator
        self._sender = sender
        self._weather = weather

    async def report(self, data: History) -> None:
        weathers = await self._get_weathers(data.data)
        report = self._generator.generate(data.data, weathers)
        await self._sender.send(data.user, report)

    async def _get_weathers(self, data: list[Measurement]) -> dict[date, Weather]:
        weathers: dict[date, Weather] = {}

        for m in data:
            d = m.date.date()
            if d in weathers:
                continue
            weathers[d] = await self._weather.get(d)

        return weathers
