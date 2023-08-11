#!/bin/sh

python manage.py compilemessages --settings=imagesizator.settings
python manage.py collectstatic --no-input
python manage.py migrate

gunicorn imagesizator.wsgi:application \
    --name imagesizator \
    --bind 0.0.0.0:8000 \
    --workers 5 \
    --log-level=info \
    --timeout 120 \
    --worker-class gevent \
"$@"
