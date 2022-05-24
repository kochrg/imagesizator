# syntax=docker/dockerfile:1

# NOTE: build-context = project-root folder

FROM ubuntu:21.04
WORKDIR /var/www/imagesizator/

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
RUN apt-get install -y openssl && \
    mkdir /etc/ssl/server-certificates && \
    cd /etc/ssl/server-certificates && \
    openssl req -newkey rsa:2048 -nodes -keyout server-key.pem -x509 -days 365 -out server-certificate.pem && \
    openssl x509 -text -noout -in server-certificate.pem && \
    openssl pkcs12 -inkey key.pem -in server-certificate.pem -export -out server-certificate.p12 && \
    openssl pkcs12 -in server-certificate.p12 -noout -info

# Adding MinTLSV1 compatibility
COPY ./docker/dockerfiles/production-web-dockerfile/conf/openssl.cnf /etc/ssl/

# Config project env
RUN apt install python3.9 python3.9-dev python3.9-distutils python3-pip python3.9-venv -y
RUN pip3 install virtualenv
RUN pip3 install virtualenvwrapper

# TODO from here
# Install mod_wsgi
RUN apt install apache2-utils ssl-cert libapache2-mod-wsgi-py3 -y

# Copy code: from project-root to www/imagesizator, this is only to build
# the container, when this Dockerfile is used in a docker-compose file
# and the volumes are mapped, the files are overwritten
COPY . /var/www/imagesizator/
COPY ./docker/dockerfiles/production-web-dockerfile/conf/django/manage.py /var/www/imagesizator/manage.py
COPY ./docker/dockerfiles/production-web-dockerfile/conf/django/pytest.ini /var/www/imagesizator/pytest.ini
COPY ./docker/dockerfiles/production-web-dockerfile/conf/django/asgi.py /var/www/imagesizator/apimutual/asgi.py
COPY ./docker/dockerfiles/production-web-dockerfile/conf/django/wsgi.py /var/www/imagesizator/apimutual/wsgi.py

# Creating venv
RUN python3 -m venv /usr/share/.virtualenvs/imagesizator
RUN echo "export PYTHONPATH='/usr/bin/python3.9'" >> /usr/share/.virtualenvs/imagesizator/bin/activate
RUN /usr/share/.virtualenvs/imagesizator/bin/pip3 install -r requirements.txt
RUN pip3 install -r requirements.txt
RUN chmod 777 -R /usr/share/.virtualenvs

COPY ./docker/dockerfiles/production-web-dockerfile/conf/ssl/cert.pem /etc/apache2/ssl/cert.pem
COPY ./docker/dockerfiles/production-web-dockerfile/conf/ssl/privkey.pem /etc/apache2/ssl/privkey.pem
COPY ./docker/dockerfiles/production-web-dockerfile/conf/ssl/chain.pem /etc/apache2/ssl/chain.pem

# Adding apache host
COPY ./docker/dockerfiles/production-web-dockerfile/conf/apimutual1.conf /etc/apache2/sites-available/apimutual1.conf
RUN a2enmod ssl
RUN a2enmod wsgi
RUN a2ensite apimutual1.conf

RUN service apache2 restart

# Starting apache2 service
CMD apachectl -DFOREGROUND