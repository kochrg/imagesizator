# Copy this file inside this django folder and rename it as 'otlp_config.py'.
from api.common.utils.api_functions import get_parameter_value

# Send otlp data?
enable_value = get_parameter_value("enable_otlp")
if enable_value == "yes":
    enable_value = True
else:
    enable_value = False

# Name of the service. Choose the name you want.
otlp_resource_attributes = get_parameter_value("otlp_resource_attributes")
if not otlp_resource_attributes:
    otlp_resource_attributes = "imagesizator-service"

# Your SigNoz server
# SigNoz common port:4317
otlp_endpoint_url = get_parameter_value("otlp_endpoint_url")
if not otlp_endpoint_url:
    otlp_endpoint_url = "http://127.0.0.1:4317"

# The endpoint uses SSL?
insecure_endpoint = get_parameter_value("otlp_insecure_endpoint")
if insecure_endpoint == "no":  # Secure server
    insecure_endpoint = False

# FINAL CONFIG
ENABLE = enable_value
OTEL_RESOURCE_ATTRIBUTES = otlp_resource_attributes
OTEL_EXPORTER_OTLP_ENDPOINT = otlp_endpoint_url
INSECURE_ENDPOINT = insecure_endpoint
