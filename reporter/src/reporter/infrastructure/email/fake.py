import asyncio
import random
from pathlib import Path

from reporter.application.dto import Report
from reporter.application.interfaces import ReportSender
from reporter.domain.models import User


class FakeEmailSender(ReportSender):
    def __init__(self, reports_path: Path) -> None:
        self._reports_path = reports_path

    async def send(self, user: User, report: Report) -> None:
        with open(self._reports_path / f"{user.email}_{report.filename}", "wb") as f:  # noqa: ASYNC230
            f.write(report.payload)

        await asyncio.sleep(random.randint(1, 10) / 10)  # noqa: S311
