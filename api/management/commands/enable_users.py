from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from rest_framework.authtoken.models import Token

User = get_user_model()


# Check if the users have a token, if not creates one
class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            users_query = User.objects.all()

            for user in users_query:
                Token.objects.get_or_create(user=user)

            print("Tokens created successfully.")
        except Exception as e:
            print(e)
