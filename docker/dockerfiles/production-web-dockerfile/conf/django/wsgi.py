# type: ignore
"""
WSGI config for imagesizator project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter  # noqa
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.wsgi import OpenTelemetryMiddleware
from django.core.wsgi import get_wsgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'imagesizator.settings_prod')

application = get_wsgi_application()

try:
    import imagesizator.otlp_config as otlp
except ImportError as error:
    print(error)

# Enable Open Telemetry?
if otlp.ENABLE:
    resource = Resource.create(attributes={
        "service.name": otlp.OTEL_RESOURCE_ATTRIBUTES
    })

    trace.set_tracer_provider(TracerProvider(resource=resource))

    span_processor = BatchSpanProcessor(
        OTLPSpanExporter(
            endpoint=otlp.OTEL_EXPORTER_OTLP_ENDPOINT,
            insecure=otlp.INSECURE_ENDPOINT
        )
    )

    trace.get_tracer_provider().add_span_processor(span_processor)

    application = OpenTelemetryMiddleware(
        application,
        None,
        None,
        trace.get_tracer_provider()
    )