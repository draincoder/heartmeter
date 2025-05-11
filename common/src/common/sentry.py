import sentry_sdk
from pydantic import BaseModel, Field


class SentryConfig(BaseModel):
    dsn: str = Field(alias="SENTRY_DSN", default="")
    enabled: bool = Field(alias="SENTRY_ENABLED", default=False)


def setup_sentry(config: SentryConfig, service_name: str) -> None:
    if config.enabled:
        sentry_sdk.init(
            dsn=config.dsn,
            server_name=service_name,
            traces_sample_rate=0,
        )
