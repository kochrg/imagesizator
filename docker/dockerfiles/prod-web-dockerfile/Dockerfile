### STAGE I - BUILD APPLICATION
FROM python:3.8-slim-buster AS builder

# Set env variables used in this Dockerfile (add a unique prefix, such as DOCKYARD)
# Directory in container for all project files
ENV DOCKYARD_SRVHOME=/srv
# Directory in container for project source files
ENV DOCKYARD_SRVPROJ=/srv/imagesizator
ENV COLUMNS=80

RUN apt-get update && apt-get install -y \
  build-essential \
  autoconf \
  libtool \
  pkg-config \
  python3-dev \
  python-cffi \
  gcc \
  g++ \
  git \
  curl \
  postgresql-client \
  libpq-dev \
  libffi-dev \
  musl-dev \
  locales \
  tzdata \
  gettext \
  && rm -rf /var/lib/apt/lists/*

# Configure timezone and locale
ENV TZ="America/Argentina/Cordoba"
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Create application subdirectories
WORKDIR $DOCKYARD_SRVHOME
RUN mkdir -p www logs www/public www/public/static www/public/temp
RUN mkdir -p www/protected www/protected/static www/protected/temp
VOLUME ["$DOCKYARD_SRVHOME/logs/"]

ADD docker-entrypoint.sh /

RUN mkdir $DOCKYARD_SRVPROJ
ADD requirements.txt $DOCKYARD_SRVPROJ/
WORKDIR $DOCKYARD_SRVPROJ

RUN python -m pip install --upgrade pip
RUN pip install django Cython
RUN pip install -r requirements.txt
RUN pip install gunicorn[gevent] requests[security]

# copy source and install dependencies
WORKDIR /opt/app

COPY requirements.txt ./
RUN pip install -r requirements.txt

### STAGE II - RUN APPLICATION
FROM python:3.8-slim-buster

# Set env variables used in this Dockerfile (add a unique prefix, such as DOCKYARD)
# Directory in container for all project files
ENV DOCKYARD_SRVHOME=/srv
# Directory in container for project source files
ENV DOCKYARD_SRVPROJ=/srv/imagesizator
ENV COLUMNS=80

RUN apt-get update && apt-get install -y libpq-dev gettext

COPY --from=builder /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

ADD . $DOCKYARD_SRVPROJ

RUN rm -f $DOCKYARD_SRVPROJ/imagesizator/.env
RUN rm -f $DOCKYARD_SRVPROJ/imagesizator/local_settings.py
RUN rm -f $DOCKYARD_SRVPROJ/imagesizator/secrets.py

# Port to expose
EXPOSE 8000

WORKDIR $DOCKYARD_SRVPROJ

# RUN python manage.py compilemessages
RUN python manage.py collectstatic --noinput

# Copy entrypoint script into the image
COPY --from=builder /docker-entrypoint.sh ./

RUN ["chmod", "+x", "./docker-entrypoint.sh"]

CMD ["./docker-entrypoint.sh"]