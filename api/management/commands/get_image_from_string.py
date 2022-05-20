from django.core.management.base import BaseCommand

import base64


# Check if the users have a token, if not creates one
class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            image_path = input("Enter the PATH and name to save the image: ")
            string_image = input("Paste the image string: ")

            with open(image_path, "wb") as image_file:
                bytes_image = base64.b64decode(string_image)
                image_file.write(bytes_image)
                image_file.close()
        except Exception as e:
            print(e)