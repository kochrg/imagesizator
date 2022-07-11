from tempfile import NamedTemporaryFile
from django.http import JsonResponse
from django.core.files.base import ContentFile
from rest_framework.generics import RetrieveAPIView
from rest_framework import permissions
from PIL import Image

import base64

from api.common.utils.api_functions import get_named_temporary_file, get_parameter_value, get_publish_file_path


# User must be logged to use this endpoint.
# Use 'Authorization: Token the_token' header.
class PILImageResize(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        response_data = {"error": "api_error"}
        response_code = 500

        try:
            # Get POST data
            # action = request.data["action"] - NOT USED -
            to_width = int(request.data["to_width"])
            to_height = int(request.data["to_height"])
            suffix = request.data["suffix"]

            # bytes image in format: base64.b64encode(image).decode('utf8')
            image = base64.b64decode(request.data["image"])

            # publish the image or send string back?
            publish = False
            temporal = False
            try:
                publish = True if request.data["publish"] == 'yes' else False
                temporal = True if request.data["temporal"] == 'yes' else False
            except Exception as e:
                print(e)

            image_thumbnail = Image.open(
                ContentFile(image, "temp_image" + suffix)
            )
            image_thumbnail.thumbnail((to_width, to_height))

            # Saving resized image to a temporal file
            # NOTE: must be used image_thumbnail.save() as the function used
            # for save the image, other saving methods didn't work (fails when saving).
            # Use image_thumbnail.tobytes() to avoid save the file
            # (using memory buffer) fails too.
            # TODO: check if there is a faster way.

            resized_image_file = get_named_temporary_file('pil_resized_', suffix, publish, temporal)
            image_thumbnail.save(resized_image_file.name)

            if publish:
                publish_url = get_publish_file_path(temporal)
                image_url = get_parameter_value('imagesizator_domain')
                image_url += publish_url + resized_image_file.name.split('/')[-1]

                response_data = {
                    'status': 'resized',
                    'width': to_width,
                    'height': to_height,
                    'suffix': suffix,
                    'image': image_url,
                }
                response_code = 200
            else:
                img_bytes = resized_image_file.read()
                string_image = base64.b64encode(img_bytes).decode('utf8')

                response_data = {
                    'status': 'resized',
                    'width': to_width,
                    'height': to_height,
                    'suffix': suffix,
                    'image': string_image,
                }
                response_code = 200
        except Exception as e:
            print(e)
            response_data = {'error': e}
            response_code = 500

        resized_image_file.close()
        return JsonResponse(response_data, status=response_code)
