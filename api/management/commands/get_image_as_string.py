import logging
import base64


from django.core.management.base import BaseCommand


# Return an image string to be used in a JSON request
class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            image_path = input("Enter the FULL PATH to the image: ")

            with open(image_path, "rb") as image_file:
                image = base64.b64encode(image_file.read()).decode(
                    "utf8"
                )  # -> bytes_string
                logging.log(1, str(image))
        except Exception as e:
            logging.log(1, e)
