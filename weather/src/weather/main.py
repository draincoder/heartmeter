import logging

import uvicorn

from common.logger import setup_logger
from .config import read_config
from .api import app

logger = logging.getLogger(__name__)


def main() -> None:
    config = read_config()
    setup_logger(config.log)

    logger.info("Starting application")
    uvicorn.run(app, host=config.api.host, port=config.api.port, log_config=None)
    logger.info("Application stopped")


if __name__ == "__main__":
    main()
