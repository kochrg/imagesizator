from django.core.management.base import BaseCommand
from django.utils.timezone import now as timezone_now

from api.models import ImagesizatorTemporaryFile

# Test endpoint with an image stored in local disk.
# Useful to test with big images.
class Command(BaseCommand):

    def handle(self, *args, **options):
        #try:
        files_query = ImagesizatorTemporaryFile.objects.filter(expiration_date__lt=timezone_now())

        for file in files_query:
            file.delete()

        # except Exception as e:
        #     print("Error deleting:", e)
