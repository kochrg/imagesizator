import base64

from django.http import JsonResponse
from rest_framework.generics import RetrieveAPIView
from rest_framework import permissions

from api.models import ImagesizatorTemporaryFile, ImagesizatorStaticFile, ImagesizatorFile
from api.common.functions.opencv import opencv_image_resize, new_opencv_image_resize
from api.common.functions.pillow import pillow_image_resize
from api.common.utils.api_functions import \
    get_parameter_value, \
    get_publish_file_path, \
    get_file_expiration_date


# User must be logged to use this endpoint.
# Use 'Authorization: Token the_token' header.
class ImageResizeView(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, service, *args, **kwargs):
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

            keep_proportion = 'none'
            try:
                keep_proportion = request.data["keep_proportion"] if request.data["keep_proportion"] else "none"
            except Exception:
                print("Parameter keep_proportion missed.")

            resized_image_file = None
            string_image = None
            if service == "opencv":
                resized_image_file, string_image, final_w_h = opencv_image_resize(
                    publish,
                    temporal,
                    image,
                    to_width,
                    to_height,
                    keep_proportion,
                    suffix
                )
            
            if service == "pillow":
                resized_image_file, string_image, final_w_h = pillow_image_resize(
                    publish,
                    temporal,
                    image,
                    to_width,
                    to_height,
                    keep_proportion,
                    suffix
                )

            # Create an entry for the file created
            if temporal:
                # as temporal
                imagesizator_temporary_file = ImagesizatorTemporaryFile(
                    path=str(resized_image_file.name),
                    bytes_string=string_image,
                )
                imagesizator_temporary_file.save(seconds=get_file_expiration_date(request))
            else:
                # as static file
                imagesizator_file = ImagesizatorFile(
                    path=str(resized_image_file.name),
                    bytes_string=string_image,
                )
                imagesizator_file.save()

            response_code = 200
            if publish:
                publish_url = get_publish_file_path(temporal)
                image_url = get_parameter_value('imagesizator_domain')
                image_url += publish_url + resized_image_file.name.split('/')[-1]

                response_data = {
                    'status': 'resized',
                    'width': final_w_h[0],
                    'height': final_w_h[1],
                    'suffix': suffix,
                    'image': image_url,
                }
            else:
                # Return image as string
                response_data = {
                    'status': 'resized',
                    'width': final_w_h[0],
                    'height': final_w_h[1],
                    'suffix': suffix,
                    'image': string_image,
                }
        except Exception as e:
            print(e)

        # TODO: check if it is possible to close (and then delete) files asynchonously
        resized_image_file.close()

        return JsonResponse(response_data, status=response_code)


# ######################################################################
# ###################### API V1.1 ######################################
# ######################################################################
# Endpoints used since version 1.1 of Imagesizator


# User must be logged to use this endpoint.
# Use 'Authorization: Token the_token' header.
class NewPublishImageResizeView(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, service,  protected="public", static="temp", *args, **kwargs):
        response_data = {"error": "api_error"}
        response_code = 500

        try:
            # Get POST data
            # action = request.data["action"] - NOT USED YET -
            to_width = int(request.data["to_width"])
            to_height = int(request.data["to_height"])
            suffix = request.data["suffix"]

            # bytes image in format: base64.b64encode(image).decode('utf8')
            decoded_image = base64.b64decode(request.data["file"])

            is_protected = bool(protected == "protected")
            is_static = bool(static == "static")

            keep_proportion = 'none'
            try:
                keep_proportion = request.data["keep_proportion"] if request.data["keep_proportion"] else "none"
            except Exception:
                print("Parameter keep_proportion missed.")

            resized_image_file = None
            string_image = None
            if service == "opencv":
                resized_image_file, string_image, final_w_h = new_opencv_image_resize(
                    publish,
                    temporal,
                    decoded_image,
                    to_width,
                    to_height,
                    keep_proportion,
                    suffix
                )
            
            if service == "pillow":
                resized_image_file, string_image, final_w_h = pillow_image_resize(
                    publish,
                    temporal,
                    decoded_image,
                    to_width,
                    to_height,
                    keep_proportion,
                    suffix
                )

            if is_static:
                # STATIC FILE
                published_file = ImagesizatorStaticFile(
                    is_protected=is_protected,
                    bytes_string=string_image,
                )
                published_file.save(
                    decoded_file=string_image,
                    suffix=suffix,
                )
            else:
                # TEMP FILE
                published_file = ImagesizatorTemporaryFile(
                    is_protected=is_protected,
                    bytes_string=string_image,
                )
                published_file.save(
                    decoded_file=string_image,
                    suffix=suffix,
                    seconds=request.data["expiration"]
                )


            # publish the image or send string back?
            publish = False
            temporal = False
            try:
                publish = True if request.data["publish"] == 'yes' else False
                temporal = True if request.data["temporal"] == 'yes' else False
            except Exception as e:
                print(e)





            # Create an entry for the file created
            if temporal:
                # as temporal
                imagesizator_temporary_file = ImagesizatorTemporaryFile(
                    path=str(resized_image_file.name),
                    bytes_string=string_image,
                )
                imagesizator_temporary_file.save(seconds=get_file_expiration_date(request))
            else:
                # as static file
                imagesizator_file = ImagesizatorFile(
                    path=str(resized_image_file.name),
                    bytes_string=string_image,
                )
                imagesizator_file.save()

            response_code = 200
            if publish:
                publish_url = get_publish_file_path(temporal)
                image_url = get_parameter_value('imagesizator_domain')
                image_url += publish_url + resized_image_file.name.split('/')[-1]

                response_data = {
                    'status': 'resized',
                    'width': final_w_h[0],
                    'height': final_w_h[1],
                    'suffix': suffix,
                    'image': image_url,
                }
            else:
                # Return image as string
                response_data = {
                    'status': 'resized',
                    'width': final_w_h[0],
                    'height': final_w_h[1],
                    'suffix': suffix,
                    'image': string_image,
                }
        except Exception as e:
            print(e)

        # TODO: check if it is possible to close (and then delete) files asynchonously
        resized_image_file.close()

        return JsonResponse(response_data, status=response_code)