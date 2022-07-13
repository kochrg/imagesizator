from django.views.generic import View 
from django.http import HttpResponse, HttpResponseServerError, HttpResponseForbidden
from django.core.management import call_command

from api.common.utils.api_functions import get_parameter_value

# Call to command delete_expired_files
class DeleteExpiredFilesView(View):
    def get(self, request, *args, **kwargs):
        print('Call to delete_expired_files.')
        remote_address = request.META['REMOTE_ADDR']
        print("Request from ADDR:", request.META['REMOTE_ADDR'])

        allowed = ['10.22.13.1', '10.22.13.2', '10.22.13.3', '127.0.0.1']
        user_allowed = get_parameter_value('imagesizator_user_allowed_hosts')

        if user_allowed:
            for ip in user_allowed.split(','):
                allowed.append(ip)

        if remote_address in allowed:
            try:
                call_command('delete_expired_files')
            except Exception as e:
                print("Error deleting files:", e)
                return HttpResponseServerError({'error': e})

            return HttpResponse('ok')
        
        return HttpResponseForbidden('Forbidden')