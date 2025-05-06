import os
from dataclasses import dataclass

from pydantic import BaseModel, Field

from common.logger import LogConfig


class APIConfig(BaseModel):
    host: str = Field(alias="API_HOST", default="127.0.0.1")
    port: int = Field(alias="API_PORT", default=8080)


@dataclass
class AppConfig:
    api: APIConfig
    log: LogConfig


def read_config() -> AppConfig:
    return AppConfig(
        api=APIConfig(**os.environ),
        log=LogConfig(**os.environ),
    )
