"""
WSGI config for imagesizator project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.wsgi import OpenTelemetryMiddleware
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'imagesizator.settings_prod')

OTEL_RESOURCE_ATTRIBUTES = 'api-service'
OTEL_EXPORTER_OTLP_ENDPOINT = "http://192.168.0.9:4317"

resource = Resource.create(attributes={
    "service.name": OTEL_RESOURCE_ATTRIBUTES
})

trace.set_tracer_provider(TracerProvider(resource=resource))

span_processor = BatchSpanProcessor(
    OTLPSpanExporter(endpoint=OTEL_EXPORTER_OTLP_ENDPOINT, insecure=True)
)

trace.get_tracer_provider().add_span_processor(span_processor)

application = get_wsgi_application()
application = OpenTelemetryMiddleware(application, None, None, trace.get_tracer_provider())
