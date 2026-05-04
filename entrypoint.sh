#!/bin/bash

set -xe
python manage.py migrate --noinput
exec gunicorn jano.wsgi:application --bind 0.0.0.0:8000 --workers 3