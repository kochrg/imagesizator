import logging

from django.views.generic import View
from django.http import HttpResponse, HttpResponseServerError, HttpResponseForbidden
from django.core.management import call_command

from api.models.core import Parameters


# Call to command delete_expired_files
class DeleteExpiredFilesView(View):
    def get(self, request, *args, **kwargs):
        logging.log(1, "Call to delete_expired_files.")
        remote_address = request.META["REMOTE_ADDR"]
        logging.log(1, "Request from ADDR:", request.META["REMOTE_ADDR"])

        allowed = ["10.22.26.1", "10.22.26.2", "10.22.26.3", "10.22.26.4", "127.0.0.1"]
        user_allowed = Parameters.get_parameter_value("imagesizator_user_allowed_hosts")

        if user_allowed:
            for ip in user_allowed.split(","):
                allowed.append(ip)

        if remote_address in allowed:
            try:
                call_command("delete_expired_files")
            except Exception as e:
                logging.log(1, "Error deleting files:", e)
                return HttpResponseServerError({"error": e})

            return HttpResponse("ok")

        return HttpResponseForbidden("Forbidden")
