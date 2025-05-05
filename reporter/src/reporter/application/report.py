from reporter.application.dto import History
from reporter.application.interfaces import ReportGenerator, ReportSender


class ReportInteractor:
    def __init__(self, generator: ReportGenerator, sender: ReportSender) -> None:
        self._generator = generator
        self._sender = sender

    async def report(self, data: History) -> None:
        report = self._generator.generate(data.data)
        await self._sender.send(data.user, report)
