import logging

import uvicorn

from common.logger import setup_logger
from common.sentry import setup_sentry
from .config import read_config
from .api import app, RequestIDMiddleware

logger = logging.getLogger(__name__)


def main() -> None:
    service_name = "weather"
    config = read_config()
    setup_logger(config.log)
    setup_sentry(config.sentry, service_name)

    app.add_middleware(RequestIDMiddleware)
    logger.info("Starting application")
    uvicorn.run(app, host=config.api.host, port=config.api.port, log_config=None)
    logger.info("Application stopped")


if __name__ == "__main__":
    main()
