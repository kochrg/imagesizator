from django.contrib.auth import get_user_model, authenticate
from django.core.management.base import BaseCommand
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

        if not Parameters.objects.filter(key='enable_otlp'):
            enable_otlp = Parameters(
                key='enable_otlp',
                value='no'
            )
            enable_otlp.save()

        if not Parameters.objects.filter(key='otlp_resource_attributes'):
            otlp_resource_attributes = Parameters(
                key='otlp_resource_attributes',
                value='imagesizator-service'
            )
            otlp_resource_attributes.save()

        if not Parameters.objects.filter(key='otlp_endpoint_url'):
            otlp_endpoint_url = Parameters(
                key='otlp_endpoint_url',
                value='http://127.0.0.1:4317'
            )
            otlp_endpoint_url.save()

        if not Parameters.objects.filter(key='otlp_insecure_endpoint'):
            otlp_insecure_endpoint = Parameters(
                key='otlp_insecure_endpoint',
                value='yes'  # insecure by default
            )
            otlp_insecure_endpoint.save()
