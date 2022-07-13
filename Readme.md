# Imagesizator
Imagesizator can receive an image through an HTTP or HTTPS endpoint, manipulate it, and send you the result.

## Prerequisites
1. Install docker:
```shell
sudo apt update && sudo apt install docker.io
```
2. Install docker-compose CLI following [this link](https://docs.docker.com/compose/install/compose-plugin/#install-the-plugin-manually).

*NOTE: if you don't know which option follow to install, the **Linux Standalone Binary** option is recommended.*

## First steps
If you want to try or test the project, you can run in a **dev mode** with Django ``manage.py runserver`` option:
1. Go to the project root folder.
2. Create a virtual environment for the project (recommended):
```shell
# Config project env
apt install python3.9 python3.9-dev python3.9-distutils python3-pip python3.9-venv -y
pip3 install virtualenv
pip3 install virtualenvwrapper

python3 -m venv /usr/share/.virtualenvs/imagesizator
echo "export PYTHONPATH='/usr/bin/python3.9'" >> /usr/share/.virtualenvs/imagesizator/bin/activate
workon imagesizator
pip3 install -r requirements.txt

# Initialize
python manage.py initadmin

# start the server
python manage.py runserver
```

### Configuring apache (deploy with docker):

1. Create a copy of *docker/dockerfiles/production-web-dockerfile/conf/imagesizator-sample.conf* inside the same folder with the name *imagesizator.conf*.
2. Customize the file with your own email, ServerName, ServerAlias and domain.
3. By default, server **listen in port 80 and 443**. If you want only one, modify the *imagesizator.conf* file created in **step 1**.
4. Using SSL:

**Creating self-signed certificates:**
If you want to use your self-signed certificates follow the next steps:
1. Go to *docker/dockerfiles/production-web-dockerfile/conf/ssl* and run: ``sh ./create-certificates.sh`` as non-root user.
2. The command will create two files inside *./server-certificates* folder: ``server.key`` and ``server.crt``. Both files are used to encrypt the connection.
3. You don't need to change anything in ``imagesizator.conf`` file.

*NOTE: there is no certificate authority (CA) file so, in some web browsers and tools you need to add an exception for the created certificate to use it or, in other cases search for ``disable SSL Verification`` (i.e.: Postman).*

**Using certificates of an official CA:**
1. Copy the key, certificate and chain (certificate + CA certificate) inside *docker/dockerfiles/production-web-dockerfile/conf/ssl/server-certificates* folder.
2. In ``imagesizator.conf`` file, point apache to use your certificates:
```
    SSLCertificateFile /etc/apache2/ssl/your_server.crt
    
    SSLCertificateKeyFile /etc/apache2/ssl/your_server.key
    
    SSLCertificateChainFile /etc/apache2/ssl/your_chain.pem
```

*NOTE: only change **the name of the file**, not the path, it is relative to docker configuration.*

### How to get the *image_as_string* in Python:
```python
with open(path_to_the_image, "rb") as image_file:
    image_as_string = base64.b64encode(image_file.read()).decode("utf8")  # -> bytes_string
    # Then use image_as_string in data
```

**NOTE:** two methods for testing endpoints:
1. You can use ``get_image_as_string`` command to get *image_as_string* in Terminal from a local image. And then use your preferred software to test the endpoint (curl, postman).
2. Run the server (``python manage.py runserver``) and use the command ``test_endpoint_with_image`` to fully test the endpoint from Terminal using an image stored in the local disk.

### Running commands
To run a command from Terminal:
1. Run your virtual environment.
2. Go to project root folder.
3. Run: ``python manage.py name_of_the_command``

### Monitoring with SigNoz (optional)

Imagesizator is compatible with OpenTelemetry Django instrumentation that enables generation of telemetry data from a Django application. The data is then used to monitor performance of a Django application with a monitoring tool like Datadog, New Relic or SigNoz (an open-source monitoring tool).

By default, Imagesizator install all the requirements needed to use [SigNoz](https://signoz.io/docs/) when running the application from the Docker container as a production server but you need to enable to send the data to your SigNoz server to get it working.

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

## About the database
Imagesizator uses a **sqlite3** database that is initialized when the server runs for the first time. It is stored inside the database folder in the root of the project directory.

**IMPORTANT NOTE:** if you have problems running the container or experiment a *Server error (500)** when trying to access to Django admin, the cause could be the permissions of the ``database/db.sqlite3`` file, and it is related to the user that creates the database when the container is created.
One way to solve this is deleting the ``db.sqlite3`` file, start your *venv* and run:

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

If you still have problems run the following command. **NOTE:** this is insecure because you give to all users permissions to write and read the database. Run this by your own risk:
```shell
chmod 777 ./database/db.sqlite3
```

# Building and running the container
1. Inside *docker/production-server* folder, run:
```shell
docker-compose build --build-arg HOST_WWW_DATA_GID=$(id www-data -g) --build-arg HOST_USER_GID=$(id -g) --build-arg HOST_USER_GNAME=$(getent group $(id -g) | cut -d: -f1) [--build-arg HT_USER=username --build-arg HT_PASSWD=password --build-arg S_TIME=84600](optional)
```
2. Run:
```
docker-compose up -d
```

# Endpoints

## Resizing with Pillow (PIL) - *recommended*
Slightly faster than opencv.

**Endpoint URI:** ``/images/pillow``

**Method:** POST

**Headers:**
- ``Authorization: Token authorized_user_token``
- ``Content-Type: application/json``

**Data:**
```json
{
    "action": "resize",
    "to_width": "your_width",
    "to_height": "your_height",
    "suffix": "the_file_extension",
    "image": "image_as_string",
}
```

## Resizing with OpenCV
**Endpoint URI:** ``/images/opencv``

**Method:** POST

**Headers:**
- ``Authorization: Token authorized_user_token``
- ``Content-Type: application/json``

**Data:**
```json
{
    "action": "resize",
    "to_width": "your_width",
    "to_height": "your_height",
    "suffix": "the_file_extension",
    "image": "image_as_string" 
}
```
