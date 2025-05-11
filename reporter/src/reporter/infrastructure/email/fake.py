import asyncio
import random
from pathlib import Path

from opentelemetry import trace

from reporter.application.dto import Report
from reporter.application.interfaces import ReportSender
from reporter.domain.models import User

tracer = trace.get_tracer(__name__)


class FakeEmailSender(ReportSender):
    def __init__(self, reports_path: Path) -> None:
        self._reports_path = reports_path

    @tracer.start_as_current_span("send email")
    async def send(self, user: User, report: Report) -> None:
        with open(self._reports_path / f"{user.email}_{report.filename}", "wb") as f:  # noqa: ASYNC230
            f.write(report.payload)

        await asyncio.sleep(random.randint(1, 10) / 10)  # noqa: S311
