import base64

from django.http import JsonResponse
from rest_framework.generics import RetrieveAPIView
from rest_framework import permissions

from api.common.utils.api_functions import \
    get_file_expiration_date, \
    get_named_temporary_file, \
    get_publish_file_path
from api.models import ImagesizatorTemporaryFile, ImagesizatorFile, Parameters


# User must be logged to use this endpoint.
# Use 'Authorization: Token the_token' header.
class PublishPDFFile(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        response_data = {"error": "api_error"}
        response_code = 500

        try:
            # Get POST data
            # action = request.data["action"] - NOT USED YET -
            suffix = '.pdf'

            # bytes image in format: base64.b64encode(image).decode('utf8')
            image = base64.b64decode(request.data["image"])

            # publish the image or send string back?
            publish = True  # Always True
            temporal = False
            try:
                temporal = True if request.data["temporal"] == 'yes' else False
            except Exception as e:
                print(e)

            pdf_image_file = get_named_temporary_file('pdf_', suffix, publish, temporal)
            pdf_image_file.write(image)

            # Create an entry for the file created
            if temporal:
                imagesizator_temporary_file = ImagesizatorTemporaryFile(
                    path=str(pdf_image_file.name),
                    bytes_string=request.data["image"],
                )
                imagesizator_temporary_file.save(seconds=get_file_expiration_date(request))
            else:
                imagesizator_file = ImagesizatorFile(
                    path=str(pdf_image_file.name),
                    bytes_string=request.data["image"],
                )
                imagesizator_file.save()      

            publish_url = get_publish_file_path(temporal)
            image_url = Parameters.get_parameter_value('imagesizator_domain')
            image_url += publish_url + pdf_image_file.name.split('/')[-1]

            response_data = {
                'status': 'published',
                'suffix': suffix,
                'image': image_url,
            }
            response_code = 200

            # TODO: check if it is possible to close (and then delete) files asynchonously
            pdf_image_file.close()
        except Exception as e:
            print(e)

        return JsonResponse(response_data, status=response_code)
