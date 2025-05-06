import os
from dataclasses import dataclass
from pathlib import Path

from common.logger import LogConfig

from reporter.presentation.rmq.config import RMQConfig


@dataclass
class AppConfig:
    rmq: RMQConfig
    log: LogConfig
    reports_path: Path
    weather_base_url: str


def read_config() -> AppConfig:
    return AppConfig(
        rmq=RMQConfig(**os.environ),
        log=LogConfig(**os.environ),
        reports_path=Path(os.environ.get("REPORTS_PATH", "./reports")),
        weather_base_url=os.environ["WEATHER_BASE_URL"],
    )
