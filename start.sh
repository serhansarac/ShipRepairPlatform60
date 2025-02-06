#!/bin/bash
apt update && apt install -y libgobject-2.0-0 libcairo2 libffi-dev libpango1.0-dev
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn ShipRepairPlatform60.wsgi:application --bind 0.0.0.0:8000
