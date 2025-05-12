import logging

import uvicorn
from asgi_monitor.integrations.fastapi import (
    MetricsConfig,
    setup_metrics,
    TracingConfig,
    setup_tracing as setup_api_tracing,
)
from asgi_monitor.logging.uvicorn import build_uvicorn_log_config
from prometheus_client import CollectorRegistry

from common.logger import setup_logger
from common.pyroscope import setup_pyroscope
from common.sentry import setup_sentry
from common.tracing import setup_tracing
from .config import read_config
from .api import app, RequestIDMiddleware

logger = logging.getLogger(__name__)


def main() -> None:
    service_name = "weather"
    config = read_config()
    setup_logger(config.log)
    setup_sentry(config.sentry, service_name)
    provider = setup_tracing(config.trace, service_name)
    setup_pyroscope(config.pyroscope, service_name)

    registry = CollectorRegistry()
    metrics_config = MetricsConfig(
        app_name=service_name,
        registry=registry,
        include_metrics_endpoint=True,
    )
    trace_config = TracingConfig(tracer_provider=provider)

    app.add_middleware(RequestIDMiddleware)
    setup_metrics(app, metrics_config)
    setup_api_tracing(app, trace_config)

    logger.info("Starting application")
    log_config = build_uvicorn_log_config(
        level=config.log.level,
        json_format=config.log.json_enabled,
        include_trace=config.log.trace_enabled,
    )
    uvicorn.run(app, host=config.api.host, port=config.api.port, log_config=log_config)
    logger.info("Application stopped")


if __name__ == "__main__":
    main()
