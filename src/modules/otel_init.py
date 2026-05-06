import logging
from loguru import logger
import sys
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter

OTEL_ENDPOINT = "http://localhost:4318"

def init_telemetry(service_name: str) -> trace.Tracer:
    resource = Resource.create({"service.name": service_name})

    trace_provider = TracerProvider(resource=resource)
    trace_provider.add_span_processor(
        BatchSpanProcessor(
            OTLPSpanExporter(endpoint=OTEL_ENDPOINT + "/v1/traces")

        )
    )
    trace.set_tracer_provider(trace_provider)

    log_provider = LoggerProvider(resource=resource)
    log_provider.add_log_record_processor(
        BatchLogRecordProcessor(
            OTLPLogExporter(endpoint=OTEL_ENDPOINT + "/v1/logs")
        )
    )
    set_logger_provider(log_provider)

    handler = LoggingHandler()
    logger.remove()
    logger.add(sink=sys.stderr, level="DEBUG")
    logger.add(sink=handler, format="{message}", level="DEBUG")

    return trace.get_tracer(service_name)