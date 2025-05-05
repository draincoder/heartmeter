import datetime
from abc import abstractmethod
from typing import Protocol

from reporter.application.dto import Report, Weather
from reporter.domain.models import Measurement, User


class ReportSender(Protocol):
    @abstractmethod
    async def send(self, user: User, report: Report) -> None: ...


class ReportGenerator(Protocol):
    @abstractmethod
    def generate(self, data: list[Measurement], weathers: dict[datetime.date, Weather]) -> Report: ...


class WeatherReader(Protocol):
    @abstractmethod
    async def get(self, date: datetime.date) -> Weather: ...
