from fileinput import filename
from tempfile import TemporaryFile, NamedTemporaryFile
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.core.files.base import ContentFile
from rest_framework.generics import RetrieveAPIView
from rest_framework import permissions

import base64
import cv2


# User must be logged to use this endpoint.
# Use 'Authorization: Token the_token' header
class OpenCVImageResize(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        response_data = {"error": "api_error"}
        response_code = 500

        try:
            # Get POST data
            # action = request.data["action"] - NOT USED -
            to_width = int(request.data["to_width"])
            to_height = int(request.data["to_height"])
            suffix = '.' + request.data["suffix"]
            
            # bytes image in format: base64.b64.encode(image).decode('utf8')
            image = base64.b64decode(request.data["image"])

            # Need to save the image from request because cv2.imread only works with a path
            with NamedTemporaryFile("wb", suffix=suffix) as f:
                f.write(image)
                processed_image = cv2.imread(f.name)
                processed_image = cv2.resize(processed_image, (to_width, to_height))

                # Saving resized image to a temporal file
                # NOTE: must be used cv2.imwrite as the function used for save the image,
                # other saving methods didn't work (fails when trying to save the image).
                # Use processed_image.tobytes() to avoid save the file (using memory buffer) fails too.
                # TODO: check if there is a faster way.
                with NamedTemporaryFile("r+b", prefix='ocv_resized_', suffix=suffix) as resized_image_file:
                    cv2.imwrite(resized_image_file.name, processed_image)
                
                    img_bytes = resized_image_file.read()
                    string_image = base64.b64encode(img_bytes).decode('utf8')

                    response_data = {
                        'status': 'resized',
                        'width': to_width,
                        'height': to_height,
                        'image': string_image,
                    }
                    response_code = 200

                    # # ---------------- TESTING --------------------
                    # with open("/tmp/skyline_testing_rebuild.jpg", "wb") as rebuild_image:
                    #     rebuild_image.write(base64.b64decode(string_image))
                    #     rebuild_image.close()
                    # # ---------------------------------------------

                    resized_image_file.close()
                    f.close()
        except Exception as e:
            print(e)

        return JsonResponse(response_data, status=response_code)
