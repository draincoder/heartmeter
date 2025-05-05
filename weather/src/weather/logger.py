import logging
from logging.handlers import RotatingFileHandler


from .config import LogConfig


def setup_logger(config: LogConfig) -> None:
    logging.basicConfig(
        level=config.level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            RotatingFileHandler(
                filename=config.filepath,
                maxBytes=10 * 1024 * 1024,
                backupCount=5,
                encoding="utf-8",
            ),
        ],
    )
