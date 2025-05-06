import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

import uvicorn
from common.logger import setup_logger
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from faststream.rabbit import RabbitBroker

from diary.config import read_config
from diary.infrastructure.di import DBProvider, InteractorProvider, RMQProvider
from diary.presentation.api.middlewares.request_id import RequestIDMiddleware
from diary.presentation.api.routes.exceptions import setup_exception_handlers
from diary.presentation.api.routes.measurements import measurements_router
from diary.presentation.api.routes.reports import reports_router
from diary.presentation.api.routes.users import users_router

logger = logging.getLogger(__name__)


def main() -> None:
    config = read_config()
    setup_logger(config.log)
    logger.info("Initializing application")

    broker = RabbitBroker(url=config.rmq.url, logger=logger)
    container = make_async_container(RMQProvider(broker), DBProvider(config.pg), InteractorProvider())

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        await broker.connect()
        yield
        await broker.close()
        await container.close()
        logger.info("Container closed")

    app = FastAPI(lifespan=lifespan)

    app.add_middleware(RequestIDMiddleware)
    app.include_router(users_router)
    app.include_router(measurements_router)
    app.include_router(reports_router)

    setup_exception_handlers(app)
    setup_dishka(container, app)

    logger.info("Starting server")
    uvicorn.run(app, host=config.api.host, port=config.api.port, log_config=None)
    logger.info("Application stopped")


if __name__ == "__main__":
    main()
