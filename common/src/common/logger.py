import contextlib
import logging
import sys
import uuid
from typing import Any

import structlog
from opentelemetry import trace
from pydantic import BaseModel, Field
from structlog.typing import EventDict, WrappedLogger


class LogConfig(BaseModel):
    level: str = Field(alias="LOG_LEVEL", default="INFO")
    json_enabled: bool = Field(alias="LOG_JSON_ENABLED", default=False)
    trace_enabled: bool = Field(alias="TRACE_ENABLED", default=False)


def setup_logger(config: LogConfig) -> None:
    _setup_structlog(json_format=config.json_enabled, include_trace=config.trace_enabled)
    _setup_logging(level=config.level, json_format=config.json_enabled, include_trace=config.trace_enabled)


def _setup_structlog(*, json_format: bool, include_trace: bool) -> None:
    processors = [
        *_build_default_processors(json_format=json_format),
        structlog.processors.StackInfoRenderer(),
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.UnicodeDecoder(),  # convert bytes to str
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,  # for integration with default logging
    ]

    if include_trace:
        processors.append(extract_opentelemetry_trace_meta)

    structlog.configure_once(
        processors=processors,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


def _setup_logging(level: str | int, *, json_format: bool, include_trace: bool) -> None:
    renderer_processor = structlog.processors.JSONRenderer() if json_format else structlog.dev.ConsoleRenderer()
    default_processors = _build_default_processors(json_format=json_format)

    if include_trace:
        default_processors.append(extract_opentelemetry_trace_meta)

    logging_processors = [
        structlog.stdlib.ProcessorFormatter.remove_processors_meta,
        renderer_processor,
    ]

    formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=default_processors,
        processors=logging_processors,
    )

    handler = logging.StreamHandler(stream=sys.stdout)
    handler.set_name("default")
    handler.setLevel(level)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(level)


def additional_serialize(logger: WrappedLogger, name: str, event_dict: EventDict) -> EventDict:
    for key, value in event_dict.items():
        if isinstance(value, uuid.UUID):
            event_dict[key] = str(value)
    return event_dict


def _build_default_processors(*, json_format: bool) -> list[Any]:
    pr = [
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.ExtraAdder(),
        additional_serialize,
        structlog.dev.set_exc_info,
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S.%f", utc=True),
        structlog.processors.dict_tracebacks,
        structlog.processors.CallsiteParameterAdder(
            {
                structlog.processors.CallsiteParameter.PATHNAME,
                structlog.processors.CallsiteParameter.FILENAME,
                structlog.processors.CallsiteParameter.MODULE,
                structlog.processors.CallsiteParameter.FUNC_NAME,
                structlog.processors.CallsiteParameter.THREAD,
                structlog.processors.CallsiteParameter.THREAD_NAME,
                structlog.processors.CallsiteParameter.PROCESS,
                structlog.processors.CallsiteParameter.PROCESS_NAME,
            },
        ),
    ]
    if json_format:
        pr.insert(0, structlog.processors.format_exc_info)

    return pr


def extract_opentelemetry_trace_meta(logger: WrappedLogger, name: str, event_dict: EventDict) -> EventDict:
    with contextlib.suppress(KeyError, ValueError):
        span = trace.get_current_span()
        if not span.is_recording():
            return event_dict

        ctx = span.get_span_context()
        service_name = trace.get_tracer_provider().resource.attributes["service.name"]  # type: ignore[attr-defined]
        parent = getattr(span, "parent", None)

        event_dict["span_id"] = trace.format_span_id(ctx.span_id)
        event_dict["trace_id"] = trace.format_trace_id(ctx.trace_id)
        event_dict["service.name"] = service_name

        if parent:
            event_dict["parent_span_id"] = trace.format_span_id(parent.span_id)

    return event_dict
