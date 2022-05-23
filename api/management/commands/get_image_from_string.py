from django.core.management.base import BaseCommand

import base64


# Create an image from a given string in format b'...'
# Paste the b'...' string inside a .txt file
class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            image_path = input("Enter the PATH and name where to save the image: ")
            string_image_path = input("Enter path to image string: ")

            with open(string_image_path, "r") as string_image:
                string_from_file = string_image.read()
                string_image.close()
                print("---------------------------------------")
                print("--------String from file---------------")
                print(string_from_file)
                print("---------------------------------------")
                bytes_image = base64.b64decode(string_from_file)
                print("---------------------------------------")
                print("-----------Bytes image-----------------")
                print(bytes_image)
                print("---------------------------------------")
                with open(image_path, "wb") as image_file:
                    image_file.write(bytes_image)
                    image_file.close()
        except Exception as e:
            print(e)