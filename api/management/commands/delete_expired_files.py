from django.core.management.base import BaseCommand
from api.common.functions.delete_expired_files import delete_expired_files


# Delete expired files
class Command(BaseCommand):

    def handle(self, *args, **options):
        if delete_expired_files():
            print("Files deleted")
        else:
            print("Error deleting files")
