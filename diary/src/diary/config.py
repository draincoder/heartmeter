import os
from dataclasses import dataclass

from diary.infrastructure.db.config import PGConfig
from diary.infrastructure.log.config import LogConfig
from diary.infrastructure.rmq.config import RMQConfig
from diary.presentation.api.config import APIConfig


@dataclass
class AppConfig:
    pg: PGConfig
    api: APIConfig
    log: LogConfig
    rmq: RMQConfig


def read_config() -> AppConfig:
    return AppConfig(
        pg=PGConfig(**os.environ),
        api=APIConfig(**os.environ),
        log=LogConfig(**os.environ),
        rmq=RMQConfig(**os.environ),
    )
