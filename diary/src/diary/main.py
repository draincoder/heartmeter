import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

import uvicorn
from asgi_monitor.integrations.fastapi import MetricsConfig, TracingConfig, setup_metrics
from asgi_monitor.integrations.fastapi import setup_tracing as setup_api_tracing
from asgi_monitor.logging.uvicorn import build_uvicorn_log_config
from common.logger import setup_logger
from common.sentry import setup_sentry
from common.tracing import setup_tracing
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from faststream.rabbit import RabbitBroker
from faststream.rabbit.opentelemetry import RabbitTelemetryMiddleware
from faststream.rabbit.prometheus import RabbitPrometheusMiddleware
from prometheus_client import CollectorRegistry

from diary.config import read_config
from diary.infrastructure.di import DBProvider, InteractorProvider, RMQProvider
from diary.presentation.api.middlewares.request_id import RequestIDMiddleware
from diary.presentation.api.routes.exceptions import setup_exception_handlers
from diary.presentation.api.routes.measurements import measurements_router
from diary.presentation.api.routes.reports import reports_router
from diary.presentation.api.routes.users import users_router

logger = logging.getLogger(__name__)


def main() -> None:
    service_name = "diary"
    config = read_config()
    setup_logger(config.log)
    setup_sentry(config.sentry, service_name)
    provider = setup_tracing(config.trace, service_name)

    logger.info("Initializing application")
    registry = CollectorRegistry()
    prom_middleware = RabbitPrometheusMiddleware(
        registry=registry,
        app_name=service_name,
        metrics_prefix="faststream",
    )
    otel_middleware = RabbitTelemetryMiddleware(tracer_provider=provider)

    broker = RabbitBroker(url=config.rmq.url, logger=logger, middlewares=[prom_middleware, otel_middleware])
    container = make_async_container(RMQProvider(broker), DBProvider(config.pg), InteractorProvider())

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        await broker.connect()
        yield
        await broker.close()
        await container.close()
        logger.info("Container closed")

    app = FastAPI(lifespan=lifespan)

    metrics_config = MetricsConfig(
        app_name=service_name,
        registry=registry,
        include_metrics_endpoint=True,
    )
    trace_config = TracingConfig(tracer_provider=provider)

    app.add_middleware(RequestIDMiddleware)
    setup_metrics(app, metrics_config)
    setup_api_tracing(app, trace_config)

    app.include_router(users_router)
    app.include_router(measurements_router)
    app.include_router(reports_router)

    setup_exception_handlers(app)
    setup_dishka(container, app)

    logger.info("Starting server")
    log_config = build_uvicorn_log_config(
        level=config.log.level,
        json_format=config.log.json_enabled,
        include_trace=config.log.trace_enabled,
    )
    uvicorn.run(app, host=config.api.host, port=config.api.port, log_config=log_config)
    logger.info("Application stopped")


if __name__ == "__main__":
    main()
