from django.contrib.auth import get_user_model, authenticate
from django.core.management.base import BaseCommand
from utils.bcolors import bcolors

User = get_user_model()


# Creates an admin user for APP
class Command(BaseCommand):

    def handle(self, *args, **options):
        username = 'admin'
        password = 'imagesizator'

        if not User.objects.filter(username='admin').exists():
            email = 'email@example.com'
            print('Creating account for %s (%s)' % (username, email))
            admin = User.objects.create_superuser(email=email, username=username, password=password)
            admin.is_active = True
            admin.is_admin = True
            admin.save()
        else:
            print('Admin accounts can only be initialized if no Accounts exist')

            # try to login with username/password
            user = authenticate(username=username, password=password)
            if user is not None:
                # Default admin password, WARNING!!
                print(f"{bcolors.WARNING}WARNING!! You have the default admin password!!{bcolors.ENDC}")
                print(
                    f"{bcolors.WARNING}Change it from Django admin. " 
                    + f"View the Readme.md file for more details.{bcolors.ENDC}"
                )