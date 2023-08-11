# Imagesizator
Imagesizator is a service that can receive images or pdf files through an HTTP or HTTPS url using a bytes-string format, manipulate them, and send you the result. In conclusion, Imagesizator works as an image or file online bucket.

With Imagesizator, you can:
- Send an image to be resized and get the resulting bytes-string.
- Send an image to be resized and published on a public or protected URL.
- Send a file to be published on a public or protected URL.
- The files can be stored in a temporary url (setting an expiration date) or in a static url, where the file will never be deleted.

## Prerequisites
All the steps on this article were tested in a Linux environment, we don't know how Imagesizator works under Windows.

1. Install docker and docker-compose CLI
*NOTE: if you don't know which option follow to install, the **Linux Standalone Binary** option is recommended.*

2. Install python3.8

## First steps
If you want to try or test the project, you can run it in **dev mode** by executing the Django ``manage.py runserver`` command:
1. Go to the project root folder.
2. Create a virtual environment (recommended):

```shell
# Config project env
apt install python3 python3-dev python3-distutils python3-pip python3-venv -y
pip3 install virtualenv
pip3 install virtualenvwrapper

python3 -m venv /usr/share/.virtualenvs/imagesizator
echo "export PYTHONPATH='/usr/bin/python3'" >> /usr/share/.virtualenvs/imagesizator/bin/activate

# Start the venv
workon imagesizator

pip3 install -r requirements.txt

# Initialize
python manage.py initadmin

# Run Imagesizator server
python manage.py runserver
```

Then you can access the server with http://127.0.0.1:8000.

If you want the server to run outside localhost, run the server with ``python manage.py runserver 0.0.0.0:80``.


**The database:**
Imagesizator uses a **SQLite 3** database that is initialized when the server runs for the first time. It is stored inside the database folder in the root of the project directory.

**IMPORTANT NOTE:** If you have problems running the container or get a **Server Error (500)** when trying to access Django admin, the cause could be the permissions of the ``database/db.sqlite3`` file, and it is related to the user that creates the database when the container is created.
One way to solve this is to delete the ``db.sqlite3`` file, start your *venv* and run:

```shell
python manage.py initadmin

# And then run the container
cd docker
docker-compose up -d
```

It will create the database file using the current user.

If it didn't work you can try to add read and write permissions to the file:
```shell
# Generally, from project root folder
chmod 755 ./database/db.sqlite3
```

If you still have problems run the following command.
**NOTE:** this is insecure because you give permissions to all users to write, read, and execute the database. Run this by your own risk:

```shell
chmod 777 ./database/db.sqlite3
```

# Building and running the container
``S_TIME="* * * * *"  # Cron format`` (optional): when you want the deamon looks for expired images and delete it. I. e.: ``"0 0 * * *"`` means *every day at 00:00* (default).

1. Inside *docker/dockerfiles/prod-web-dockerfile* folder, run:
```shell
docker-compose build --build-arg S_TIME="* * * * *" (optional)
```
2. Run:
```
docker-compose up -d
```


### Monitoring with SigNoz or any other OpenTelemetry application (optional)

Imagesizator is compatible with OpenTelemetry Django instrumentation that enables generation of telemetry data from a Django application. The data is then used to monitor performance of a Django application with a monitoring tool like Datadog, New Relic or SigNoz (an open-source monitoring tool).

By default, Imagesizator install all the requirements needed to use [SigNoz](https://signoz.io/docs/) when running the application from the Docker container as a production server but you need to enable sending data to your SigNoz (or other) server to get it working.

**About SigNoz**
*"SigNoz is an open-source APM. It helps developers monitor their applications & troubleshoot problems, an open-source alternative to DataDog, NewRelic, etc. fire desktop_computer. point_right Open source Application Performance Monitoring (APM) & Observability tool"* [Github repository](https://github.com/SigNoz/signoz)

More info about SigNoz and Django:
- [Install SigNoz with Docker](https://signoz.io/docs/install/docker)
- [Monitoring a Django app with SigNoz](https://signoz.io/blog/opentelemetry-django/)


**Configuring Imagesizator with SigNoz**
1. Go to Django admin page: *your_imagesizator_url/admin*
2. Login
3. Go to ``Parameters`` and modify otlp parameters:
- ``enable_otlp``: set yo *yes* to enable or *no* to disable.
- ``otlp_resource_attributes``: choose the name that you want. By default *imagesizator-service*.
- ``otlp_endpoint_url``: the *remote service url*. I.e.: your SigNoz server:port.
- ``otlp_insecure_endpoint``: set to *no* if your remote service use SSL, *yes* to disable.

*Remember: if the docker container exists (was created before), you need to stop it, delete the process and run ``docker-compose up -d`` to see the new changes.*


# Endpoints

## How to get an *image_as_string* in Python
```python
with open(path_to_the_image, "rb") as image_file:
    image_as_string = base64.b64encode(image_file.read()).decode("utf8")  # -> bytes_string
    # Then use image_as_string in data
```

**NOTE:** two integrated methods for testing endpoints:
1. You can use ``get_image_as_string`` command to get an *image_as_string* in Terminal from a local image stored in your hard disk.
2. It will return the selected image as a bytes string, copy the output and then use your preferred software to test an Imagesizator endpoint (curl, postman).
3. **Or** run the server (``python manage.py runserver``) and use the command ``test_endpoint_with_image`` to fully test the endpoint from Terminal using an image stored in the local disk.


### Running commands
To run a command from Terminal:
1. Run your virtual environment.
2. Go to project root folder.
3. Run: ``python manage.py name_of_the_command``


## Working with images

**Endpoint URI:** ``<action>/image/<service>/<protected>/<static>``

**URL Parameters:**
```
action =
    - publish: publish the image in a specific folder
    - retrieve: same as publish but also returns the bytes-string of the published image
service =
    - pillow: lib to manipulate the image. Slightly faster than OpenCV
    - opencv: another lib for image manipulation
protected =
    - protected: if you want the image to be only accessed only by registered users
    - public: the image will be accessed using the URL without restrictions
static =
    - static: the file will never be deleted
    - temp: if you want the image to be available for a specific period of time
```

**Headers:**
- ``Authorization: Token authorized_user_token``
- ``Content-Type: application/json``

**Method:** POST

**Data:**
- to_width = "your_width" (integer). Final width of the resized image.
- to_height = "your_height" (integer). Final height of the resized image.
- suffix = "the_file_extension" (i. e.: ".jpg") **!important**.
- expiration (optional) = "seconds" (integer). The seconds in what the image will be available by url. Only valid when it is combined with *temp* images. Default 24 hs.
- image = the image as a bytes string.

```json
{
    "to_width": "your_width",
    "to_height": "your_height",
    "suffix": "the_file_extension",
    "expiration": "seconds",
    "image": "image_as_string",
}
```

## Publish files
**Endpoint URI:** ``publish/<protected>/<static>``

**URL Parameters:**
```
protected =
    - protected: if you want the file to be only accessed only by registered users
    - public: the file will be accessed using the URL without restrictions
static =
    - static: the file will never be deleted
    - temp: if you want the file to be available for a specific period of time
```

**Method:** POST

**Headers:**
- ``Authorization: Token authorized_user_token``
- ``Content-Type: application/json``

**Data:**
- expiration (optional) = "seconds" (integer). The seconds in what the file will be available by url. Only valid when it is combined with *temp* files. Default 24 hs.
- file = the file as a bytes string.

```json
{
    "expiration": "seconds",
    "file": "file_as_string"
}
```

# Accessing files
By default the url returned in the response of an endpoint call, points directly to the file. But, when you are working with protected images or files, you need to add the token in the last part of the url.

## Public images:
Directly use the URL returned in the response.
For example:
- with imagesizator service url: http://imagesizator.domain.com
- returned url: http://imagesizator.domain.com/www/public/*<folder>*/file_name.jpg
- *<folder>* could be **static** or **temp**
- copy and paste the URL in a web browser to access the file

## Protected images:
You need to add the user token to the URL returned in the response.
For example:
- with imagesizator service url: http://imagesizator.domain.com
- returned url: http://imagesizator.domain.com/www/public/*<folder>*/file_name.jpg
- final url: http://imagesizator.domain.com/www/public/*<folder>*/file_name.jpg/*<token>*
- *<folder>* could be **static** or **temp**
- *<token>* the token of a registered user
- copy and paste the URL in a web browser to access the file
