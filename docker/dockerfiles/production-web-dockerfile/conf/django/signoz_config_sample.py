# Copy this file inside this django folder and rename it as 'signoz_config.py'.

# Enable signoz monitoring?
ENABLE = False

# Name of the service. Choose the name you want. It will be displayed
# in the main page of SigNoz and will help you to identify the service.
OTEL_RESOURCE_ATTRIBUTES = 'imagesizator-service'

# Your SigNoz server url
OTEL_EXPORTER_OTLP_ENDPOINT = "http://localhost:4317"

# Your server is using an SSL certificate?
# True: not using SSL
# False: the server is using a SSL certificate
INSECURE_ENDPOINT = True
