# type: ignore
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

try:
    from imagesizator.signoz.config import *
except ImportError as error:
    from imagesizator.signoz.config.default import *


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'imagesizator.settings_prod')

if ENABLE_SIGNOZ:
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
else:
    application = get_wsgi_application()