# Imagesizator
Imagesizator can receive an image through an HTTP or HTTPS endpoint, manipulate it, and send you the result.

## First Steps
1. On root folder rename the file ``settings.sample-env`` to ``.env`` and change the ``SECRET_KEY=`` value.

## Running commands
To run a command from Terminal:
1. Run your virtual environment.
2. Go to project root folder.
3. Run: ``python manage.py name_of_the_command``

# Endpoints

## Resizing with OpenCV
**Endpoint URI:** ``/images/opencv``
**Method:** POST
**Headers:**
- ``Authorization: Token authorized_user_token``
- ``Content-Type: application/json``
**Data:**
```
{
    "action": "resize",
    "to_width": "your_width",
    "to_height": "your_height",
    "image": "image_as_string" 
}
```

How to get the *image_as_string* in Python:
```
with open(path_to_the_image, "rb") as image_file:
    image_as_string = base64.b64encode(image_file.read()).decode("utf8")  # -> bytes_string
    # Then use image_as_string in data
```

**NOTE:** two methods for testing:
1. You can use ``get_image_as_string`` command to get *image_as_string* in Terminal from a local image. And then use your preferred software to test the endpoint (curl, postman).
2. Run the server (``python manage.py runserver``) and use the command ``test_endpoint_with_image`` to fully test the endpoint from Terminal using an image stored in the local disk.