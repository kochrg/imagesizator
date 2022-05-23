from email import header
from django.core.management.base import BaseCommand

import base64
import json
import requests
import time

# Test endpoint with an image stored in local disk.
# Useful to test with big images.
class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            endpoint_uri = input("Enter endpoint URI: ")
            token = input("User Token: ")
            image_path = input("Enter the FULL PATH to the image: ")
            action = input("Enter the action: ")
            to_width = input("Enter the final width: ")
            to_height = input("Enter the final height: ")
            suffix = input("Enter the image suffix: ")
            
            with open(image_path, "rb") as image_file:
                image = base64.b64encode(image_file.read()).decode("utf8")  # -> bytes_string
                data = {
                    "action": action,
                    "to_width": to_width,
                    "to_height": to_height,
                    "suffix": suffix,
                    "image": image,
                }
                headers = {'Authorization': 'Token ' + token}
                start_time = time.time()
                response = requests.post(endpoint_uri, data=data, headers=headers)
                end_time = time.time()
                print(response)
                print(json.loads(response.text))
                print("Endpoint execution time: %s seconds" % (end_time - start_time))
        except Exception as e:
            print(e)