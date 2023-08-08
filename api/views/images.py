import base64

from django.http import JsonResponse
from rest_framework.generics import RetrieveAPIView
from rest_framework import permissions

from api.models.core import ImagesizatorFile
from api.models.imagesizator_image_file import ImagesizatorImageFile
from api.common.functions.opencv import opencv_image_resize
from api.common.functions.pillow import pillow_image_resize
from api.common.utils.api_functions import \
    get_parameter_value, \
    get_publish_file_path


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

            # 'image' is in format: base64.b64encode(image).decode('utf8')
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
                imagesizator_temporary_file = ImagesizatorFile(
                    path=str(resized_image_file.name),
                    bytes_string=string_image,
                    is_static=False,
                    is_protected=False
                )
                imagesizator_temporary_file.set_file_expiration_date(seconds=int(request.data['expiration']))
                imagesizator_temporary_file.save()
            else:
                # as static file
                imagesizator_file = ImagesizatorFile(
                    path=str(resized_image_file.name),
                    bytes_string=string_image,
                    is_static=True,
                    is_protected=False,
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
                expiration = request.data["expiration"] if request.data["expiration"] else "none"
            except Exception:
                print("Parameter expiration missed.")

            print("Creating imagesizator file")
            image_file = ImagesizatorImageFile(
                is_protected=is_protected,
                is_static=is_static,
                bytes_string=decoded_file,
                suffix=suffix
            )

            print("Setting expiration_date")
            if image_file.is_temporal:
                image_file.set_file_expiration_date(expiration)

            if service == "opencv":
                print("Starting resize")
                image_file.opencv_image_resize(
                    to_width,
                    to_height,
                    suffix,
                    keep_proportion
                )
                print("Resize successfull")
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
