from stat import S_IRWXG, S_IRWXU
from tempfile import NamedTemporaryFile
from django.http import JsonResponse
from rest_framework.generics import RetrieveAPIView
from rest_framework import permissions

import os
import base64
import cv2

from api.common.utils.api_functions import get_parameter_value, get_static_path, get_temp_path


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
                # other saving methods didn't work (fails when trying to save the image).
                # Use processed_image.tobytes() to avoid save the file (using memory buffer) fails too.
                # TODO: check if there is a faster way.
                if publish:
                    # Return image public url
                    publish_path = ''
                    publish_url = ''
                    if temporal:
                        publish_path = get_temp_path()
                        publish_url = '/public/temp/'
                    else:
                        # static file
                        publish_path = get_static_path()
                        publish_url = '/public/static/'

                    with NamedTemporaryFile(
                        "r+b",
                        prefix='ocv_resized_',
                        suffix=suffix,
                        dir=publish_path,
                        delete=False
                    ) as resized_image_file:
                        cv2.imwrite(resized_image_file.name, processed_image)

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

                        # chmod 770 (Grant rwx access to www-data.www-data 'user.group')
                        os.chmod(resized_image_file.name, S_IRWXU + S_IRWXG)
                        resized_image_file.close()
                        f.close()
                else:
                    # Return image as string
                    with NamedTemporaryFile("r+b", prefix='ocv_resized_', suffix=suffix) as resized_image_file:
                        cv2.imwrite(resized_image_file.name, processed_image)

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

                        # TODO: check if it is possible to close (and then delete)
                        # files asynchonously
                        resized_image_file.close()
                        f.close()
        except Exception as e:
            print(e)

        return JsonResponse(response_data, status=response_code)
