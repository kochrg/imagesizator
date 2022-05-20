from django.core.management.base import BaseCommand

import base64


# Check if the users have a token, if not creates one
class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            image_path = input("Enter the FULL PATH to the image: ")
            
            with open(image_path, "rb") as image_file:
                image = base64.b64encode(image_file.read()).decode("utf8")
                print(str(image))
        except Exception as e:
            print(e)