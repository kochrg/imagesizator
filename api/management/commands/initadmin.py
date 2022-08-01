from django.contrib.auth import get_user_model, authenticate
from django.core.management.base import BaseCommand
from api.common.utils.api_functions import add_parameter_if_not_exists
from api.common.utils.bcolors import bcolors
from api.models import Parameters

User = get_user_model()


# Creates an admin user for APP
class Command(BaseCommand):

    def handle(self, *args, **options):
        username = 'admin'
        password = 'imagesizator'

        if not User.objects.filter(username='admin').exists():
            email = 'email@example.com'
            print('Creating account for %s (%s)' % (username, email))
            admin = User.objects.create_superuser(
                email=email,
                username=username,
                password=password
            )
            admin.is_active = True
            admin.is_admin = True
            admin.save()
        else:
            print('Admin accounts can only be initialized if no Accounts exist')

            # try to login with username/password
            user = authenticate(username=username, password=password)
            if user is not None:
                # Default admin password, WARNING!!
                print(
                    f"{bcolors.WARNING}WARNING!! You have the \
                        default admin password!!{bcolors.ENDC}"
                )
                print(
                    f"{bcolors.WARNING}Change it from Django admin. "
                    + f"View the Readme.md file for more details.{bcolors.ENDC}"
                )

        print(f"{bcolors.OKBLUE}Adding imagesizator parameters if not exists.{bcolors.ENDC}")

        add_parameter_if_not_exists('enable_otlp', 'no')
        add_parameter_if_not_exists('otlp_resource_attributes', 'imagesizator-service')
        add_parameter_if_not_exists('otlp_endpoint_url', 'http://127.0.0.1:4317')
        add_parameter_if_not_exists('otlp_insecure_endpoint', 'yes')
        add_parameter_if_not_exists('imagesizator_user_allowed_hosts', 'None')