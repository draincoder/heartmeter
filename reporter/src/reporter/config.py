import os
from dataclasses import dataclass
from pathlib import Path

from common.logger import LogConfig
from common.sentry import SentryConfig
from pydantic import BaseModel, Field

from reporter.presentation.rmq.config import RMQConfig


class MetricsAPIConfig(BaseModel):
    host: str = Field(alias="API_HOST", default="127.0.0.1")
    port: int = Field(alias="API_PORT", default=8080)


@dataclass
class AppConfig:
    rmq: RMQConfig
    log: LogConfig
    sentry: SentryConfig
    reports_path: Path
    weather_base_url: str
    metrics: MetricsAPIConfig


def read_config() -> AppConfig:
    return AppConfig(
        rmq=RMQConfig(**os.environ),
        log=LogConfig(**os.environ),
        sentry=SentryConfig(**os.environ),
        reports_path=Path(os.environ.get("REPORTS_PATH", "./reports")),
        weather_base_url=os.environ["WEATHER_BASE_URL"],
        metrics=MetricsAPIConfig(**os.environ),
    )
