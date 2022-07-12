from django.views.generic import View 
from django.http import HttpResponse, HttpResponseServerError, HttpResponseForbidden
from django.core.management import call_command

# Call to command delete_expired_files
class DeleteExpiredFilesView(View):
    def get(self, request, *args, **kwargs):
        print('Call to delete_expired_files.')
        remote_address = request.META['REMOTE_ADDR']
        print("Request from ADDR:", request.META['REMOTE_ADDR'])

        allowed = ['10.22.13.2', '127.0.0.1']
        if remote_address in allowed:
            try:
                call_command('delete_expired_files')
            except Exception as e:
                print("Error deleting files:", e)
                return HttpResponseServerError({'error': e})

            return HttpResponse('ok')
        
        return HttpResponseForbidden('Forbidden')