import base64
import logging

from django.http import JsonResponse
from rest_framework.generics import RetrieveAPIView
from rest_framework import permissions

from api.models.core import ImagesizatorFile


# ######################################################################
# ###################### API V1.1 ######################################
# ######################################################################
# Endpoints used since version 1.1 of Imagesizator

# User must be logged to use this endpoint.
# Use 'Authorization: Token the_token' header.
class NewPublishFile(RetrieveAPIView):
    """
    Publish any type of file without modifications.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, protected="public", static="temp", *args, **kwargs):
        response_data = {"error": "api_error"}
        response_code = 500

        try:
            # Get POST data
            # action = request.data["action"] - NOT USED YET -
            suffix = request.data["suffix"]

            # bytes file in format: base64.b64encode(file).decode('utf8')
            decoded_file = base64.b64decode(request.data["file"])

            is_protected = protected == "protected"
            is_static = static == "static"

            imagesizator_file = ImagesizatorFile(
                is_protected=is_protected,
                is_static=is_static,
                bytes_string=decoded_file,
                suffix=suffix,
            )

            if not is_static:
                # Temp file: look for expiration
                seconds = int(request.data.get("expiration", 0))
                if seconds > 0:
                    imagesizator_file.set_file_expiration_date(seconds)

            imagesizator_file.save()

            response_data = {
                "status": "published",
                "suffix": suffix,
                "file_url": imagesizator_file.url,
            }
            response_code = 200

        except Exception as e:
            logging.log(1, e)

        return JsonResponse(response_data, status=response_code)
