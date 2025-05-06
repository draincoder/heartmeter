import logging
import uuid

import uvicorn

from common.logger import setup_logger
from .config import read_config
from .api import app, RequestIDMiddleware

logger = logging.getLogger(__name__)


def main() -> None:
    config = read_config()
    setup_logger(config.log)

    app.add_middleware(RequestIDMiddleware)
    logger.info("Starting application")
    uvicorn.run(app, host=config.api.host, port=config.api.port, log_config=None)
    logger.info("Application stopped")


if __name__ == "__main__":
    main()
