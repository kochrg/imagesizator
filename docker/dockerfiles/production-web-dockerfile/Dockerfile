# syntax=docker/dockerfile:1

# NOTE: build-context = project-root folder

FROM ubuntu:21.04
WORKDIR /var/www/imagesizator/

ENV TZ=America/Argentina
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install needed packages
RUN apt update
RUN apt upgrade -y

# Install nano for edition
RUN apt install nano -y

# Install apache2
RUN apt install apache2 -y

# Create self-signed certificates by default
# Replace inside ssl folder to use custom certificates
# Installing certificates
RUN apt-get install -y openssl

# Installing certificates
COPY ./docker/dockerfiles/production-web-dockerfile/conf/ssl/server-certificates/* /etc/apache2/ssl/

# Config project env
RUN apt install python3.9 python3.9-dev python3.9-distutils python3-pip python3.9-venv -y
RUN pip3 install virtualenv
RUN pip3 install virtualenvwrapper

# Install mod_wsgi
RUN apt install apache2-utils ssl-cert libapache2-mod-wsgi-py3 -y

# Copy code: from project-root to www/imagesizator, if you make changes in a file
# call to docker-compose build
COPY . /var/www/imagesizator/
COPY ./docker/dockerfiles/production-web-dockerfile/conf/django/manage.py /var/www/imagesizator/manage.py
COPY ./docker/dockerfiles/production-web-dockerfile/conf/django/pytest.ini /var/www/imagesizator/pytest.ini
COPY ./docker/dockerfiles/production-web-dockerfile/conf/django/asgi.py /var/www/imagesizator/imagesizator/asgi.py
COPY ./docker/dockerfiles/production-web-dockerfile/conf/django/wsgi.py /var/www/imagesizator/imagesizator/wsgi.py

# Creating venv
RUN python3 -m venv /usr/share/.virtualenvs/imagesizator
RUN echo "export PYTHONPATH='/usr/bin/python3.9'" >> /usr/share/.virtualenvs/imagesizator/bin/activate
RUN /usr/share/.virtualenvs/imagesizator/bin/pip3 install -r requirements.txt
RUN chmod 777 -R /usr/share/.virtualenvs

# Creating database and applying migrations
RUN /usr/share/.virtualenvs/imagesizator/bin/python manage.py migrate

# Creating superuser
RUN /usr/share/.virtualenvs/imagesizator/bin/python manage.py initadmin

# Setting opentelemetry
RUN /usr/share/.virtualenvs/imagesizator/bin/opentelemetry-bootstrap --action=install

# Adding staticfiles
RUN /usr/share/.virtualenvs/imagesizator/bin/python manage.py collectstatic --no-input

# Change folder owner
RUN chown -R www-data:www-data /var/www/imagesizator

# Adding apache host
COPY ./docker/dockerfiles/production-web-dockerfile/conf/imagesizator.conf /etc/apache2/sites-available/imagesizator.conf
RUN a2enmod ssl
RUN a2enmod wsgi
RUN a2ensite imagesizator.conf

RUN service apache2 restart

# Starting apache2 service
CMD apachectl -DFOREGROUND