from tempfile import NamedTemporaryFile
from django.http import JsonResponse
from rest_framework.generics import RetrieveAPIView
from rest_framework import permissions

import base64
import cv2

from api.models import ImagesizatorTemporaryFile
from api.common.utils.api_functions import \
    get_named_temporary_file, \
    get_parameter_value, \
    get_publish_file_path, \
    get_file_expiration_date


# User must be logged to use this endpoint.
# Use 'Authorization: Token the_token' header.
class OpenCVImageResize(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        response_data = {"error": "api_error"}
        response_code = 500

        try:
            # Get POST data
            # action = request.data["action"] - NOT USED YET -
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

            # Need to save the image from request because cv2.imread only works with a path
            with NamedTemporaryFile("wb", suffix=suffix) as f:
                f.write(image)
                processed_image = cv2.imread(f.name)
                processed_image = cv2.resize(processed_image, (to_width, to_height))

                # Saving resized image to a temporal file and make it public
                # NOTE: must be used cv2.imwrite as the function used for save the image,
                # other saving methods didn't work (fails when trying to save the image),
                # use of processed_image.tobytes() and avoid save the file also (memory buffer).
                # TODO: check if there is a faster way.

                resized_image_file = get_named_temporary_file(
                    'ocv_resized_',
                    suffix,
                    publish,
                    temporal
                )
                cv2.imwrite(resized_image_file.name, processed_image)

                img_bytes = resized_image_file.read()
                string_image = base64.b64encode(img_bytes).decode('utf8')

                # Create an entry for the file created
                imagesizator_temporary_file = ImagesizatorTemporaryFile(
                    path=str(resized_image_file.name),
                    bytes_string=string_image,
                )
                imagesizator_temporary_file.save(seconds=get_file_expiration_date(request))

                response_code = 200
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
                else:
                    # Return image as string
                    response_data = {
                        'status': 'resized',
                        'width': to_width,
                        'height': to_height,
                        'suffix': suffix,
                        'image': string_image,
                    }
        except Exception as e:
            print(e)

        # TODO: check if it is possible to close (and then delete) files asynchonously
        resized_image_file.close()
        f.close()
        return JsonResponse(response_data, status=response_code)
