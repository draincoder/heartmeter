from faststream import Context
from faststream.rabbit import RabbitRouter
from typing_extensions import Annotated

from reporter.application.dto import History
from reporter.application.report import ReportInteractor

router = RabbitRouter()


@router.subscriber("reports")
async def generate_report(data: History, interactor: Annotated[ReportInteractor, Context()]) -> None:
    await interactor.report(data)
