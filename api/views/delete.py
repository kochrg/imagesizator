import logging

from django.http import JsonResponse
from rest_framework.generics import RetrieveAPIView
from rest_framework import permissions

from api.models.core import ImagesizatorFile


# ######################################################################
# ###################### API V1.1 ######################################
# ######################################################################
# Endpoints used since version 1.1 of Imagesizator

# User must be logged to use this endpoint.
# Use 'Authorization: Token the_token' header.
class DeleteFile(RetrieveAPIView):
    """
    Delete a file.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(
        self,
        request,
        protected="public",
        static="temp",
        file_name=None,
        *args,
        **kwargs
    ):
        response_data = {"error": "api_error"}
        response_code = 500

        try:

            is_protected = protected == "protected"
            is_static = static == "static"

            imagesizator_file = ImagesizatorFile.objects.get(
                is_protected=is_protected, is_static=is_static, file_name=file_name
            )

            if imagesizator_file.created_by == request.user:
                imagesizator_file.delete()

                response_data = {
                    "status": "deleted",
                    "file_name": file_name,
                }
                response_code = 200
            else:
                response_data = {
                    "status": "forbidden",
                    "file_name": file_name,
                }
                response_code = 403

        except ImagesizatorFile.DoesNotExist as e:
            logging.log(1, e)
            response_data = {"error": "Bad filename"}
            response_code = 404
        except Exception as e:
            logging.log(1, e)

        return JsonResponse(response_data, status=response_code)
