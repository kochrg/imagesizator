from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


# Creates an admin user for APP
class Command(BaseCommand):

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            username = 'admin'
            email = 'email@example.com'
            password = 'imagesizator'
            print('Creating account for %s (%s)' % (username, email))
            admin = User.objects.create_superuser(email=email, username=username, password=password)
            admin.is_active = True
            admin.is_admin = True
            admin.save()
        else:
            print('Admin accounts can only be initialized if no Accounts exist')
