"""
WSGI config for imagesizator project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
from opentelemetry.instrumentation.wsgi import OpenTelemetryMiddleware
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'imagesizator.settings_prod')

OTEL_RESOURCE_ATTRIBUTES = {'service.name': 'api-service'}
OTEL_EXPORTER_OTLP_ENDPOINT = "http://localhost:4317"

application = get_wsgi_application()
application = OpenTelemetryMiddleware(application)