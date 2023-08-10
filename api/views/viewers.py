import logging

from django.http import HttpResponse, FileResponse
from rest_framework.authtoken.models import Token
from rest_framework.generics import RetrieveAPIView

from api.models.core import ImagesizatorFile


class PublicBrowserFileViewer(RetrieveAPIView):
    permission_classes = []

    def get(self, request, folder, file_name, *args, **kwargs):
        """
        Return a FileResponse to open the file in a web browser
        """
        try:

            imagesizator_file = ImagesizatorFile.objects.get(
                file_name=file_name, is_static=(folder == "static")
            )

            if ("public/" + folder) in imagesizator_file.path:
                file = open(imagesizator_file.path, "rb")  # noqa
                response = FileResponse(file)

                return response
        except ImagesizatorFile.DoesNotExist:
            return HttpResponse("Not Found", status=404)
        except Exception as e:
            logging.log(1, "Error (Public browser viewer):", e)

        return HttpResponse("Error", status=500)


class ProtectedBrowserFileViewer(RetrieveAPIView):
    permission_classes = []

    def get(self, request, folder, file_name, token, *args, **kwargs):
        """
        Return a FileResponse to open the file in a web browser
        """
        try:
            # Check if it is a valid token
            token_query = Token.objects.filter(key=token)
            if token is None or not token_query.exists():
                return HttpResponse("Forbidden", status=403)

            imagesizator_file = ImagesizatorFile.objects.get(
                file_name=file_name, is_static=(folder == "static")
            )

            if ("protected/" + folder) in imagesizator_file.path:
                file = open(imagesizator_file.path, "rb")  # noqa
                response = FileResponse(file)

                return response
        except ImagesizatorFile.DoesNotExist:
            return HttpResponse("Not Found", status=404)
        except Exception as e:
            logging.log(1, "Error (Protected browser viewer):", e)

        return HttpResponse("Error", status=500)


class UnsecureProtectedBrowserFileViewer(RetrieveAPIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        """
        Accessing protected file without token.
        Return forbidden.
        """

        return HttpResponse("Forbidden", status=403)
