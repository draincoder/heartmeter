import pyroscope
from pydantic import BaseModel, Field


class PyroscopeConfig(BaseModel):
    endpoint: str = Field(alias="PYROSCOPE_ENDPOINT", default="")
    enabled: bool = Field(alias="PYROSCOPE_ENABLED", default=False)


def setup_pyroscope(config: PyroscopeConfig, service_name: str) -> None:
    if not config.enabled:
        return

    pyroscope.configure(
        application_name=service_name,
        server_address=config.endpoint,
    )
