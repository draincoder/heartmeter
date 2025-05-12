import os
from dataclasses import dataclass

from pydantic import BaseModel, Field

from common.logger import LogConfig
from common.pyroscope import PyroscopeConfig
from common.sentry import SentryConfig
from common.tracing import TraceConfig


class APIConfig(BaseModel):
    host: str = Field(alias="API_HOST", default="127.0.0.1")
    port: int = Field(alias="API_PORT", default=8080)


@dataclass
class AppConfig:
    api: APIConfig
    log: LogConfig
    sentry: SentryConfig
    trace: TraceConfig
    pyroscope: PyroscopeConfig


def read_config() -> AppConfig:
    return AppConfig(
        api=APIConfig(**os.environ),
        log=LogConfig(**os.environ),
        sentry=SentryConfig(**os.environ),
        trace=TraceConfig(**os.environ),
        pyroscope=PyroscopeConfig(**os.environ),
    )
