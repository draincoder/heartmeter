from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from pydantic import BaseModel, Field


class TraceConfig(BaseModel):
    endpoint: str = Field(alias="TRACE_ENDPOINT", default="")
    enabled: bool = Field(alias="TRACE_ENABLED", default=False)


def setup_tracing(config: TraceConfig, service_name: str) -> TracerProvider | None:
    if not config.enabled:
        return None

    resource = Resource.create(attributes={"service.name": service_name})
    tracer_provider = TracerProvider(resource=resource)
    exporter = OTLPSpanExporter(endpoint=config.endpoint)
    processor = BatchSpanProcessor(exporter)
    tracer_provider.add_span_processor(processor)
    trace.set_tracer_provider(tracer_provider)
    return tracer_provider
