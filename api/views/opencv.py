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

        # try:
        # Get POST data
        # action = request.data["action"] - NOT USED -
        to_width = int(request.data["to_width"])
        to_height = int(request.data["to_height"])
        print(str(request.data["image"]))
        image = base64.b64decode(str(request.data["image"])) # bytes image

        print(image)

        with NamedTemporaryFile("wb", delete=False) as f:
            f.write(image)
            f.close()
            processed_image = cv2.imread(f.name)
            processed_image = cv2.resize(processed_image, (to_width, to_height))

            # processed_image = cv2.imencode('.jpg', processed_image)
            cv2.imwrite("/tmp/skyline_resized.jpg", processed_image)            

            with open("/tmp/skyline_resized.jpg", "rb") as processed_image:
                img_bytes = processed_image.read()
                string_image = base64.b64encode(img_bytes).decode('utf8')

                response_data = {
                    'status': 'resized',
                    'width': to_width,
                    'height': to_height,
                    'image': string_image,
                }
                response_code = 200

                # ---------------- TESTING --------------------
                with open("/tmp/skyline_testing_rebuild.jpg", "wb") as rebuild_image:
                    rebuild_image.write(base64.b64decode(string_image))
                    rebuild_image.close()
                # ---------------------------------------------

                processed_image.close()
        # except Exception as e:
        #     print(e)

        return JsonResponse(response_data, status=response_code)
