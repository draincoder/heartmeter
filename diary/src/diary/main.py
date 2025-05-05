import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

import uvicorn
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from diary.config import read_config
from diary.infrastructure.di import DBProvider, InteractorProvider
from diary.infrastructure.log.setup import setup_logger
from diary.presentation.api.routes.exceptions import setup_exception_handlers
from diary.presentation.api.routes.measurements import measurements_router
from diary.presentation.api.routes.users import users_router

logger = logging.getLogger(__name__)


def main() -> None:
    config = read_config()
    setup_logger(config.log)
    logger.info("Initializing application")

    container = make_async_container(DBProvider(config.pg), InteractorProvider())

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        yield
        await container.close()
        logger.info("Container closed")

    app = FastAPI(lifespan=lifespan)
    app.include_router(users_router)
    app.include_router(measurements_router)

    setup_exception_handlers(app)
    setup_dishka(container, app)

    logger.info("Starting server")
    uvicorn.run(app, host=config.api.host, port=config.api.port, log_config=None)
    logger.info("Application stopped")


if __name__ == "__main__":
    main()
