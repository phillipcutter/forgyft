#!/bin/bash


# Migrate DB changes
echo Attempting to migrate DB changes
python manage.py migrate

# Collectstatic
echo Collecting Staticfiles
python manage.py collectstatic --no-input


# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn forgyft.wsgi:application \
    --bind 0.0.0.0:80 \
    --workers 2