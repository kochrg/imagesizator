from fileinput import filename
from tempfile import TemporaryFile, NamedTemporaryFile
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.files.base import ContentFile
from rest_framework.generics import RetrieveAPIView
from rest_framework import permissions
from PIL import Image

import base64


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

            image_thumbnail = Image.open(ContentFile(image, "temp_image" + suffix))
            image_thumbnail.thumbnail((to_width, to_height))
            
            # Saving resized image to a temporal file
            # NOTE: must be used image_thumbnail.save() as the function used for save the image,
            # other saving methods didn't work (fails when saving).
            # Use image_thumbnail.tobytes() to avoid save the file (using memory buffer) fails too.
            # TODO: check if there is a faster way.
            with NamedTemporaryFile("r+b", prefix='pil_resized_', suffix=suffix) as resized_image_file:
                image_thumbnail.save(resized_image_file.name)
            
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
                resized_image_file.close()
        except Exception as e:
            print(e)

        return JsonResponse(response_data, status=response_code)