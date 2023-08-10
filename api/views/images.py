import base64

from django.http import JsonResponse
from rest_framework.generics import RetrieveAPIView
from rest_framework import permissions

from api.models.imagesizator_image_file import ImagesizatorImageFile


# ######################################################################
# ###################### API V1.1 ######################################
# ######################################################################
# Endpoints used since version 1.1 of Imagesizator


# User must be logged to use this endpoint.
# Use 'Authorization: Token the_token' header.
class PublishRetrieveImageResizeView(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, action, service,  protected="public", static="temp", *args, **kwargs):
        response_data = {"error": "api_error"}
        response_code = 500

        try:
            # Get POST data
            to_width = int(request.data["to_width"])
            to_height = int(request.data["to_height"])
            suffix = request.data["suffix"]

            # 'file' is in format: base64.b64encode(image).decode('utf8')
            decoded_file = base64.b64decode(request.data["file"])

            is_protected = bool(protected == "protected")
            is_static = bool(static == "static")

            keep_proportion = 'none'
            try:
                keep_proportion = request.data["keep_proportion"] if request.data["keep_proportion"] else "none"
            except Exception:
                print("Parameter keep_proportion missed.")

            expiration = 'none'
            try:
                expiration = request.data["expiration"] if request.data["expiration"] else None
            except Exception:
                print("Parameter expiration missed.")

            image_file = ImagesizatorImageFile(
                is_protected=is_protected,
                is_static=is_static,
                bytes_string=decoded_file,
                suffix=suffix
            )

            if image_file.is_temporal:
                image_file.set_file_expiration_date(expiration)

            if service == "opencv":
                image_file.opencv_image_resize(
                    to_width,
                    to_height,
                    suffix,
                    keep_proportion
                )
            elif service == "pillow":
                image_file.pillow_image_resize(
                    to_width,
                    to_height,
                    suffix,
                    keep_proportion
                )

            image_file.save()
            response_code = 200
            response_data = {
                'status': 'resized',
                'width': image_file.width,
                'height': image_file.height,
                'suffix': image_file.suffix,
                'image_url': image_file.url,
            }
            if action == 'retrieve':
                response_data['bytes_string'] = image_file.string_image

        except Exception as e:
            print(e)

        return JsonResponse(response_data, status=response_code)
