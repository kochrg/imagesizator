# Copy this file inside this django folder and rename it as 'signoz.config.py'.

# Enable signoz monitoring?
ENABLE_SIGNOZ=False

# Name of the service. Choose the name you want.
OTEL_RESOURCE_ATTRIBUTES = 'imagesizator-service'

# Your SigNoz server
OTEL_EXPORTER_OTLP_ENDPOINT = "http://localhost:4317"

# The endpoint uses SSL?
INSECURE_ENDPOINT=True