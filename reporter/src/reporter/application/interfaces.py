from abc import abstractmethod
from typing import Protocol

from reporter.application.dto import Report
from reporter.domain.models import Measurement, User


class ReportSender(Protocol):
    @abstractmethod
    async def send(self, user: User, report: Report) -> None: ...


class ReportGenerator(Protocol):
    @abstractmethod
    def generate(self, data: list[Measurement]) -> Report: ...
