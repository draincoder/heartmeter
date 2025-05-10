import logging
import sys
import uuid
from typing import Any

import structlog
from pydantic import BaseModel, Field
from structlog.typing import EventDict, WrappedLogger


class LogConfig(BaseModel):
    level: str = Field(alias="LOG_LEVEL", default="INFO")
    json_enabled: bool = Field(alias="LOG_JSON_ENABLED", default=False)


def setup_logger(config: LogConfig) -> None:
    _setup_structlog(json_format=config.json_enabled)
    _setup_logging(level=config.level, json_format=config.json_enabled)


def _setup_structlog(*, json_format: bool) -> None:
    processors = [
        *_build_default_processors(json_format=json_format),
        structlog.processors.StackInfoRenderer(),
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.UnicodeDecoder(),  # convert bytes to str
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,  # for integration with default logging
    ]

    structlog.configure_once(
        processors=processors,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


def _setup_logging(level: str | int, *, json_format: bool) -> None:
    renderer_processor = structlog.processors.JSONRenderer() if json_format else structlog.dev.ConsoleRenderer()
    default_processors = _build_default_processors(json_format=json_format)

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
