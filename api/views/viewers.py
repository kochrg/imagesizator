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
                file_name=file_name
            )

            if ('public/' + folder) in imagesizator_file.path:
                file = open(imagesizator_file.path, 'rb')
                response = FileResponse(file)

                return response
        except ImagesizatorFile.DoesNotExist:
            return HttpResponse("Not Found", status=404)
        except Exception as e:
            print("Error (Public browser viewer):", e)

        return HttpResponse("Error", status=500)


class ProtectedBrowserFileViewer(RetrieveAPIView):
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