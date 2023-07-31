import base64

from django.http import JsonResponse, HttpResponse, FileResponse
from rest_framework.authtoken.models import Token
from rest_framework.generics import RetrieveAPIView
from rest_framework import permissions

from api.common.utils.api_functions import \
    get_file_expiration_date, \
    get_named_temporary_file, \
    get_parameter_value, \
    get_publish_file_path
from api.models import ImagesizatorTemporaryFile, ImagesizatorFile, ImagesizatorStaticFile


# User must be logged to use this endpoint.
# Use 'Authorization: Token the_token' header.
class PublishFile(RetrieveAPIView):
    """
    Publish any type of file without modifications
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        response_data = {"error": "api_error"}
        response_code = 500

        try:
            # Get POST data
            # action = request.data["action"] - NOT USED YET -
            suffix = request.data["suffix"]

            # bytes file in format: base64.b64encode(file).decode('utf8')
            file = base64.b64decode(request.data["file"])

            # publish the file or send string back?
            publish = True  # Always True
            temporal = False
            try:
                temporal = True if request.data["temporal"] == 'yes' else False
            except Exception as e:
                print(e)

            any_type_file = get_named_temporary_file('publish_' + suffix.replace(".", "") + "_", suffix, publish, temporal)
            any_type_file.write(file)

            # Create an entry for the file created
            if temporal:
                imagesizator_temporary_file = ImagesizatorTemporaryFile(
                    path=str(any_type_file.name),
                    bytes_string=request.data["file"],
                )
                imagesizator_temporary_file.save(seconds=get_file_expiration_date(request))
            else:
                imagesizator_file = ImagesizatorFile(
                    path=str(any_type_file.name),
                    bytes_string=request.data["file"],
                )
                imagesizator_file.save()

            publish_url = get_publish_file_path(temporal)
            file_url = get_parameter_value('imagesizator_domain')
            file_url += publish_url + any_type_file.name.split('/')[-1]

            response_data = {
                'status': 'published',
                'suffix': suffix,
                'file': file_url,
            }
            response_code = 200

            # TODO: check if it is possible to close (and then delete) files asynchonously
            any_type_file.close()
        except Exception as e:
            print(e)

        return JsonResponse(response_data, status=response_code)


class browserFileViewer(RetrieveAPIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        """
        Return a FileResponse to open the file in a web browser
        """
        try:
            # path could be the entire url returned by an imagesizator endpoint
            # or a path, starting from public. I. e.: public/temp/name_of_file
            url = request.GET['path']
            token = request.GET['token']

            # Check if it is a valid token
            token_query = Token.objects.filter(key=token)
            if token == None or not token_query.exists():
                return HttpResponse("Forbidden", status=403)

            # Get POST datadef pdf_view(request):
            if not url:
                return HttpResponse("Not Found", status=404)

            url_args = url.split("/")
            file_path = url_args[-3] + "/" + url_args[-2] + "/" + url_args[-1]

            file = open(file_path, 'rb')

            response = FileResponse(file)

            return response
        except Exception as e:
            print("Error (pdf_viewer):", e)

        return HttpResponse("Error", status=500)
    

# ######################################################################
# ###################### API V1.1 ######################################
# ######################################################################
# Endpoints used since version 1.1 of Imagesizator

# User must be logged to use this endpoint.
# Use 'Authorization: Token the_token' header.
class NewPublishFile(RetrieveAPIView):
    """
    Publish any type of file without modifications.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, protected="public", static="temp", *args, **kwargs):
        response_data = {"error": "api_error"}
        response_code = 500

        try:
            # Get POST data
            # action = request.data["action"] - NOT USED YET -
            suffix = request.data["suffix"]

            # bytes file in format: base64.b64encode(file).decode('utf8')
            decoded_file = base64.b64decode(request.data["file"])

            is_protected = bool(protected == "protected")
            is_static = bool(static == "static")

            published_file = None
            if is_static:
                # STATIC FILE
                published_file = ImagesizatorStaticFile(
                    is_protected=is_protected,
                    bytes_string=request.data["file"],
                )
                published_file.save(
                    decoded_file=decoded_file,
                    suffix=suffix,
                )
            else:
                # TEMP FILE
                published_file = ImagesizatorTemporaryFile(
                    is_protected=is_protected,
                    bytes_string=request.data["file"],
                )
                published_file.save(
                    decoded_file=decoded_file,
                    suffix=suffix,
                    seconds=request.data["expiration"]
                )

            response_data = {
                'status': 'published',
                'suffix': suffix,
                'file': published_file.url,
            }
            response_code = 200

        except Exception as e:
            print(e)

        return JsonResponse(response_data, status=response_code)