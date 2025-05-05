import asyncio
import logging

from faststream import FastStream, context
from faststream.rabbit import RabbitBroker

from reporter.application.report import ReportInteractor
from reporter.config import read_config
from reporter.infrastructure.email.fake import FakeEmailSender
from reporter.infrastructure.excel.generator import ExcelGenerator
from reporter.infrastructure.log.setup import setup_logger
from reporter.infrastructure.weather.client import AiohttpWeatherClient
from reporter.presentation.rmq.handler import router

logger = logging.getLogger(__name__)


async def main() -> None:
    config = read_config()
    setup_logger(config.log)
    logger.info("Initializing application")

    broker = RabbitBroker(url=config.rmq.url, logger=logger)
    broker.include_router(router)
    app = FastStream(broker, logger=logger)

    interactor = ReportInteractor(
        ExcelGenerator(),
        FakeEmailSender(config.reports_path),
        AiohttpWeatherClient(config.weather_base_url),
    )
    context.set_global("interactor", interactor)

    logger.info("Starting application")
    await app.run()
    logger.info("Application stopped")


if __name__ == "__main__":
    asyncio.run(main())
