import logging

import uvicorn
from common.logger import setup_logger
from common.pyroscope import setup_pyroscope
from common.sentry import setup_sentry
from common.tracing import setup_tracing
from faststream import context
from faststream.asgi import AsgiFastStream
from faststream.rabbit import RabbitBroker
from faststream.rabbit.opentelemetry import RabbitTelemetryMiddleware
from faststream.rabbit.prometheus import RabbitPrometheusMiddleware
from opentelemetry.instrumentation.aiohttp_client import AioHttpClientInstrumentor
from prometheus_client import CollectorRegistry, make_asgi_app

from reporter.application.report import ReportInteractor
from reporter.config import read_config
from reporter.infrastructure.email.fake import FakeEmailSender
from reporter.infrastructure.excel.generator import ExcelGenerator
from reporter.infrastructure.weather.client import AiohttpWeatherClient
from reporter.presentation.rmq.handler import router
from reporter.presentation.rmq.middleware import RequestIDMiddleware

logger = logging.getLogger(__name__)


def main() -> None:
    service_name = "reporter"
    config = read_config()
    setup_logger(config.log)
    setup_sentry(config.sentry, service_name)
    provider = setup_tracing(config.trace, service_name)
    setup_pyroscope(config.pyroscope, service_name)
    logger.info("Initializing application")

    registry = CollectorRegistry()
    prom_middleware = RabbitPrometheusMiddleware(
        registry=registry,
        app_name=service_name,
        metrics_prefix="faststream",
    )
    otel_middleware = RabbitTelemetryMiddleware(tracer_provider=provider)
    AioHttpClientInstrumentor().instrument()

    broker = RabbitBroker(
        url=config.rmq.url,
        logger=logger,
        middlewares=[RequestIDMiddleware, prom_middleware, otel_middleware],
    )
    broker.include_router(router)
    app = AsgiFastStream(broker, [("/metrics", make_asgi_app(registry))], logger=logger)

    interactor = ReportInteractor(
        ExcelGenerator(),
        FakeEmailSender(config.reports_path),
        AiohttpWeatherClient(config.weather_base_url),
    )
    context.set_global("interactor", interactor)

    logger.info("Starting application")
    uvicorn.run(app, host=config.metrics.host, port=config.metrics.port, log_config=None)
    logger.info("Application stopped")


if __name__ == "__main__":
    main()
